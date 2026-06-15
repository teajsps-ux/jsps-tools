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

function getQuestionCount(body) {
  const count = Number(body?.questionCount || 20);
  if (!Number.isFinite(count)) return 20;
  return Math.max(1, Math.min(50, Math.round(count)));
}

function buildPirlsPlan(count) {
  const labels = ["直接提取", "直接推論", "詮釋整合", "比較評估"];
  const base = Math.floor(count / labels.length);
  let remainder = count % labels.length;
  return labels.map(label => {
    const n = base + (remainder > 0 ? 1 : 0);
    remainder -= 1;
    return `${label} ${n} 題`;
  }).join("、");
}

function buildQuestionCountInstruction(body) {
  const count = getQuestionCount(body);
  return `請產生剛好 ${count} 題四選一選擇題，不要多也不要少。PIRLS 四層次請盡量平均分配：${buildPirlsPlan(count)}。`;
}

function buildPrompt(body) {
  return [
    buildQuestionCountInstruction(body),
    "你是台灣國小老師的閱讀理解出題助手，專門根據提供的教材進行內容深究出題。",
    "請根據老師提供的教材內容（可能是圖片或PDF），自動出指定題數的四選一選擇題。",
    "題目設計必須符合 PIRLS（國際閱讀素養調查）的四個理解層次，並且平均分佈（依前述題數規劃分佈）：",
    "1. 直接提取：找出課文中明確寫出的資訊",
    "2. 直接推論：連結課文中的多處資訊，找出未直接寫明但合理的推論",
    "3. 詮釋、整合觀點與訊息：歸納段落大意、比較人物角色性格、理解作者意圖或課文主旨",
    "4. 檢驗、評估內容與語言：評估課文結構、寫作手法、遣詞用字或表達效果",
    "",
    "出題要求：",
    "- 題目與選項文字必須適合國小低中年級，用語自然流暢，字句清晰，不宜過度艱深刁鑽。",
    "- 選項A、選項B、選項C、選項D的內容應該長度相當、具備合理的誘答性。",
    "- 正確答案（ans）必須是選項A、選項B、選項C或選項D中其中一個選項的「完整文字內容」，不能只寫 A、B、C、D 或 1、2、3、4，必須是完全相同的字串。",
    "- 在 notes 欄位中，簡要說明出題的設計理念，並條列各層次的題數分佈以供檢驗。",
    `教材檔名：${body.filename || "teacher-source"}`
  ].join("\n");
}

function buildYoutubePrompt(body) {
  return [
    buildQuestionCountInstruction(body),
    "你是台灣國小老師的閱讀理解出題助手，專門根據影片的字幕內容進行內容深究出題。",
    "請根據提供的影片字幕內容，自動出指定題數的四選一選擇題。",
    "題目設計必須符合 PIRLS（國際閱讀素養調查）的四個理解層次，並且平均分佈（依前述題數規劃分佈）：",
    "1. 直接提取：找出影片字幕中明確說出的資訊",
    "2. 直接推論：連結影片字幕中的多處資訊，找出未直接說明但合理的推論",
    "3. 詮釋、整合觀點與訊息：歸納段落大意、比較人物角色性格、理解作者意圖或影片主旨",
    "4. 檢驗、評估內容與語言：評估影片結構、說話手法、遣詞用字或表達效果",
    "",
    "出題要求：",
    "- 題目與選項文字必須適合國小低中年級，用語自然流暢，字句清晰，不宜過度艱深刁鑽。",
    "- 選項A、選項B、選項C、選項D的內容應該長度相當、具備合理的誘答性。",
    "- 正確答案（ans）必須是選項A、選項B、選項C或選項D中其中一個選項的「完整文字內容」，不能只寫 A、B、C、D 或 1、2、3、4，必須是完全相同的字串。",
    "- 在 notes 欄位中，簡要說明出題的設計理念，並條列各層次的題數分佈以供檢驗。",
    `影片標題：${body.filename || "youtube-video"}`
  ].join("\n");
}

function buildTextPrompt(body) {
  return [
    buildQuestionCountInstruction(body),
    "你是台灣國小老師的閱讀理解出題助手，專門根據提供的教材文章內容進行內容深究出題。",
    "請根據老師提供的教材文章內容，自動出指定題數的四選一選擇題。",
    "題目設計必須符合 PIRLS（國際閱讀素養調查）的四個理解層次，並且平均分佈（依前述題數規劃分佈）：",
    "1. 直接提取：找出教材內容中明確寫出的資訊",
    "2. 直接推論：連結教材內容中的多處資訊，找出未直接寫明但合理的推論",
    "3. 詮釋、整合觀點與訊息：歸納段落大意、比較人物角色性格、理解作者意圖或課文主旨",
    "4. 檢驗、評估內容與語言：評估課文結構、寫作手法、遣詞用字或表達效果",
    "",
    "出題要求：",
    "- 題目與選項文字必須適合國小低中年級，用語自然流暢，字句清晰，不宜過度艱深刁鑽。",
    "- 選項A、選項B、選項C、選項D的內容應該長度相當、具備合理的誘答性。",
    "- 正確答案（ans）必須是選項A、選項B、選項C或選項D中其中一個選項的「完整文字內容」，不能只寫 A、B、C、D 或 1、2、3、4，必須是完全相同的字串。",
    "- 在 notes 欄位中，簡要說明出題的設計理念，並條列各層次的題數分佈以供檢驗。",
    `教材標題：${body.filename || "teacher-source"}`
  ].join("\n");
}

function buildFileContent(body) {
  const mimeType = body.mimeType || "application/octet-stream";
  if (!body.fileBase64) throw new Error(`Missing fileBase64 for ${body.filename || "uploaded file"}.`);
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

function extractVideoId(url) {
  if (!url) return null;
  const cleaned = String(url).trim();
  if (cleaned.length === 11) return cleaned;
  try {
    const parsed = new URL(cleaned);
    if (parsed.hostname === "youtu.be") {
      return parsed.pathname.slice(1);
    }
    if (parsed.hostname.includes("youtube.com")) {
      if (parsed.pathname.startsWith("/shorts/")) {
        return parsed.pathname.split("/")[2];
      }
      return parsed.searchParams.get("v");
    }
  } catch {
    const match = cleaned.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/i);
    if (match) return match[1];
  }
  return null;
}

async function fetchYoutubeTranscript(videoId) {
  const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
  const response = await fetch(videoUrl, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
  });
  if (!response.ok) {
    throw new Error(`無法存取 YouTube 影片頁面，狀態碼: ${response.status}`);
  }
  const html = await response.text();

  let playerResponseText = null;
  const startIdx = html.indexOf("ytInitialPlayerResponse = ");
  if (startIdx !== -1) {
    const sub = html.slice(startIdx + "ytInitialPlayerResponse = ".length);
    let openBraces = 0;
    let closed = false;
    let endIdx = 0;
    for (let i = 0; i < sub.length; i++) {
      if (sub[i] === "{") openBraces++;
      else if (sub[i] === "}") {
        openBraces--;
        if (openBraces === 0) {
          endIdx = i;
          closed = true;
          break;
        }
      }
    }
    if (closed) {
      playerResponseText = sub.slice(0, endIdx + 1);
    }
  }

  if (!playerResponseText) {
    throw new Error("無法在影片網頁中解析出播放器資訊（ytInitialPlayerResponse），這可能是因為 YouTube 變更了網頁結構。");
  }

  const playerResponse = JSON.parse(playerResponseText);
  const title = playerResponse.videoDetails?.title || "YouTube影片";

  const captions = playerResponse.captions?.playerCaptionsTracklistRenderer;
  if (!captions || !captions.captionTracks || captions.captionTracks.length === 0) {
    throw new Error("此影片未提供任何字幕軌，請改選其他有字幕的影片。");
  }

  const tracks = captions.captionTracks;
  let selectedTrack = tracks.find(t => t.languageCode === "zh-TW" || t.languageCode === "zh-Hant" || t.languageCode === "zh-HK");
  let autoTranslate = false;

  if (!selectedTrack) {
    selectedTrack = tracks.find(t => t.languageCode.startsWith("zh"));
  }
  if (!selectedTrack) {
    selectedTrack = tracks.find(t => t.languageCode.startsWith("en"));
    if (selectedTrack) {
      autoTranslate = true;
    }
  }
  if (!selectedTrack) {
    selectedTrack = tracks[0];
    autoTranslate = true;
  }

  let captionUrl = selectedTrack.baseUrl;
  if (autoTranslate) {
    captionUrl += "&tlang=zh-TW";
  }
  captionUrl += "&fmt=json3";

  const captionRes = await fetch(captionUrl, {
    headers: {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
      "Referer": videoUrl,
      "Accept": "*/*",
      "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
  });

  if (!captionRes.ok) {
    if (captionRes.status === 429) {
      throw new Error(
        "YouTube 傳回 429 錯誤（拒絕存取）。這通常是 YouTube 對雲端或機房 IP 的安全防護限制。若您目前正在雲端環境執行本工具，請下載此專案程式並改在您的個人本機電腦（家用或學校 IP）開啟本機伺服器執行，即可正常抓取。"
      );
    }
    throw new Error(`無法下載該影片的字幕軌，狀態碼: ${captionRes.status}`);
  }

  const text = await captionRes.text();
  if (!text || text.length === 0) {
    throw new Error(
      "下載之字幕內容為空。這通常是 YouTube 對雲端或機房 IP 的安全防護限制。若您目前正在雲端環境執行本工具，請下載此專案程式並改在您的個人本機電腦（家用或學校 IP）開啟本機伺服器執行，即可正常抓取。"
    );
  }

  let captionJson;
  try {
    captionJson = JSON.parse(text);
  } catch {
    throw new Error("無法將下載之字幕解析為 JSON 結構。");
  }

  const lines = [];
  for (const event of captionJson.events || []) {
    if (!event.segs) continue;
    const segText = event.segs.map(s => s.utf8).join("").trim();
    if (segText) {
      lines.push(segText);
    }
  }

  const fullText = lines.join(" ");
  return { text: fullText, title };
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

  let inputContent = [];
  const questionCount = getQuestionCount(body);
  const uploadedFiles = Array.isArray(body.files)
    ? body.files
    : (Array.isArray(body.filesData) ? body.filesData : []);

  if (uploadedFiles.length > 0) {
    inputContent = [
      { type: "input_text", text: buildPrompt(body) }
    ];
    for (const file of uploadedFiles) {
      inputContent.push(buildFileContent(file));
    }
  } else if (body.textSource) {
    const filename = body.filename || "貼上教材文章";
    inputContent = [
      { type: "input_text", text: buildTextPrompt({ filename }) },
      { type: "input_text", text: `教材文章內容如下：\n\n${body.textSource}` }
    ];
  } else if (body.youtubeUrl) {
    const videoId = extractVideoId(body.youtubeUrl);
    if (!videoId) {
      throw new Error("無效的 YouTube 影片網址，請確認網址格式正確。");
    }
    const { text: transcript, title: videoTitle } = await fetchYoutubeTranscript(videoId);
    if (!transcript) {
      throw new Error("無法提取影片字幕，可能因為該影片沒有字幕或此伺服器受限於 YouTube IP 封鎖。");
    }
    const filename = `YouTube - ${videoTitle}`;
    inputContent = [
      { type: "input_text", text: buildYoutubePrompt({ filename }) },
      { type: "input_text", text: `影片字幕內容如下：\n\n${transcript}` }
    ];
  } else {
    if (!body.fileBase64) {
      throw new Error("No source file content was received. Please re-select the files and try again.");
    }
    inputContent = [
      { type: "input_text", text: buildPrompt(body) },
      buildFileContent(body)
    ];
  }

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
        content: inputContent
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
              title: { type: "string", description: "教材的主旨、標題或簡短的主題（例如：魯班的故事、一年級首冊第九課），適合用來作為下載 CSV 檔的檔名。" },
              questions: {
                type: "array",
                minItems: questionCount,
                maxItems: questionCount,
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
            required: ["title", "questions", "notes"]
          }
        }
      }
    })
  });

  if (!response.ok) throw new Error(`OpenAI failed: ${response.status} ${await response.text()}`);
  const parsed = parseJsonPayload(extractResponseText(await response.json()));
  const generatedQuestions = Array.isArray(parsed.questions) ? parsed.questions : [];
  if (generatedQuestions.length !== questionCount) {
    throw new Error(`AI returned ${generatedQuestions.length} questions, expected ${questionCount}. Please try again or choose a smaller number.`);
  }
  const csvContent = convertToCsv(generatedQuestions);
  return { csv: csvContent, notes: String(parsed.notes || ""), title: String(parsed.title || "知識王_AI題庫") };
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
