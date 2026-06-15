import http from "node:http";
import os from "node:os";
import path from "node:path";
import fs from "node:fs";

const PORT = Number(process.env.QUIZ_KING_PORT || 8787);
const MODEL = process.env.OPENAI_MODEL || "gpt-5.5";

function loadEnvFile(filePath) {
  if (!fs.existsSync(filePath)) return;
  const lines = fs.readFileSync(filePath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const [key, ...rest] = trimmed.split("=");
    if (!process.env[key]) process.env[key] = rest.join("=").trim().replace(/^["']|["']$/g, "");
  }
}

function sendJson(res, status, payload) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS"
  });
  res.end(JSON.stringify(payload));
}

function extractResponseText(responseJson) {
  if (typeof responseJson.output_text === "string") return responseJson.output_text;
  const chunks = [];
  for (const item of responseJson.output || []) {
    for (const content of item.content || []) {
      if (typeof content.text === "string") chunks.push(content.text);
    }
  }
  return chunks.join("\n").trim();
}

function parseJsonPayload(text) {
  const trimmed = String(text || "").trim();
  try {
    return JSON.parse(trimmed);
  } catch {
    const first = trimmed.indexOf("{");
    const last = trimmed.lastIndexOf("}");
    if (first !== -1 && last > first) return JSON.parse(trimmed.slice(first, last + 1));
    throw new Error("OpenAI response was not valid JSON.");
  }
}

function buildPrompt(body) {
  return [
    "你是台灣國小老師的閱讀理解出題助手，專門根據提供的教材進行內容深究出題。",
    "請根據老師提供的教材內容（可能是圖片或PDF），自動出20題四選一選擇題。",
    "題目設計必須符合 PIRLS（國際閱讀素養調查）的四個理解層次，並且平均分佈（每個層次各出 5 題，總共 20 題）：",
    "1. 直接提取：找出課文中明確寫出的資訊（共 5 題）",
    "2. 直接推論：連結課文中的多處資訊，找出未直接寫明但合理的推論（共 5 題）",
    "3. 詮釋、整合觀點與訊息：歸納段落大意、比較人物角色性格、理解作者意圖或課文主旨（共 5 題）",
    "4. 檢驗、評估內容與語言：評估課文結構、寫作手法、遣詞用字或表達效果（共 5 題）",
    "",
    "出題要求：",
    "- 題目與選項文字必須適合國小低中年級，用語自然流暢，字句清晰，不宜過度艱深刁鑽。",
    "- 選項A、選項B、選項C、選項D的內容應該長度相當、具備合理的誘答性。",
    "- 正確答案（ans）必須是選項A、選項B、選項C或選項D中其中一個選項的「完整文字內容」，不能只寫 A、B、C、D 或 1、2、3、4，必須是完全相同的字串。",
    "- 在 notes 欄位中，簡要說明出題的設計理念，並條列各層次的題數分佈以供檢驗。",
    `教材檔名：${body.filename || "teacher-source"}`
  ].join("\n");
}

function buildFileContent(body) {
  const mimeType = body.mimeType || "application/octet-stream";
  if (!body.fileBase64) throw new Error("Missing fileBase64.");
  if (mimeType.startsWith("image/")) {
    return {
      type: "input_image",
      image_url: `data:${mimeType};base64,${body.fileBase64}`
    };
  }
  if (mimeType === "application/pdf" || /\.pdf$/i.test(body.filename || "")) {
    return {
      type: "input_file",
      filename: body.filename || "source.pdf",
      file_data: `data:application/pdf;base64,${body.fileBase64}`
    };
  }
  throw new Error("目前支援圖片檔與 PDF 檔。");
}

function convertToCsv(questions) {
  const header = "題目,選項A,選項B,選項C,選項D,正確答案";
  const rows = [header];
  for (const q of questions) {
    const csvCell = (val) => {
      const clean = String(val || "").trim();
      return /[",\r\n]/.test(clean) ? `"${clean.replace(/"/g, '""')}"` : clean;
    };
    rows.push([
      csvCell(q.q),
      csvCell(q.a),
      csvCell(q.b),
      csvCell(q.c),
      csvCell(q.d),
      csvCell(q.ans)
    ].join(","));
  }
  return rows.join("\n");
}

async function generateCsv(body) {
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) throw new Error("OPENAI_API_KEY is missing from C:\\Users\\ketty\\.openai.env");

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model: MODEL,
      input: [{
        role: "user",
        content: [
          { type: "input_text", text: buildPrompt(body) },
          buildFileContent(body)
        ]
      }],
      text: {
        format: {
          type: "json_schema",
          name: "quiz_csv_result",
          strict: true,
          schema: {
            type: "object",
            additionalProperties: false,
            properties: {
              questions: {
                type: "array",
                items: {
                  type: "object",
                  additionalProperties: false,
                  properties: {
                    q: { type: "string", description: "題目內容，必須是深究教材內容的選擇題，符合該PIRLS層次的評估要求。" },
                    a: { type: "string", description: "選項A文字" },
                    b: { type: "string", description: "選項B文字" },
                    c: { type: "string", description: "選項C文字" },
                    d: { type: "string", description: "選項D文字" },
                    ans: { type: "string", description: "正確答案，必須與選項A、B、C或D的文字內容完全一致" },
                    pirls: { type: "string", description: "此題所屬的PIRLS四層次名稱之一" }
                  },
                  required: ["q", "a", "b", "c", "d", "ans", "pirls"]
                }
              },
              notes: { type: "string", description: "備註說明，例如設計理念或PIRLS題型分佈" }
            },
            required: ["questions", "notes"]
          }
        }
      }
    })
  });

  if (!response.ok) throw new Error(`OpenAI failed: ${response.status} ${await response.text()}`);
  const parsed = parseJsonPayload(extractResponseText(await response.json()));
  const csvContent = convertToCsv(parsed.questions || []);
  return { csv: csvContent, notes: String(parsed.notes || "") };
}

loadEnvFile(path.join(os.homedir(), ".openai.env"));

const server = http.createServer((req, res) => {
  if (req.method === "OPTIONS") return sendJson(res, 200, { ok: true });
  if (req.method === "GET" && req.url === "/health") return sendJson(res, 200, { ok: true, model: MODEL });
  if (req.method !== "POST" || req.url !== "/quiz-csv") return sendJson(res, 404, { error: "Not found." });

  let raw = "";
  req.on("data", chunk => { raw += chunk; });
  req.on("end", async () => {
    try {
      const body = JSON.parse(raw || "{}");
      sendJson(res, 200, await generateCsv(body));
    } catch (error) {
      sendJson(res, 500, { error: "Quiz CSV generation failed.", detail: String(error.message || error) });
    }
  });
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`Knowledge King AI helper listening at http://127.0.0.1:${PORT}`);
  console.log(`Model: ${MODEL}`);
});
