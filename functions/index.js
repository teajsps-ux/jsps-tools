"use strict";

const { onRequest } = require("firebase-functions/v2/https");
const { defineSecret } = require("firebase-functions/params");
const { GoogleGenAI } = require("@google/genai");

const GEMINI_API_KEY = defineSecret("GEMINI_API_KEY");

const normalizeCard = (card) => ({
  word: String(card?.word || "").trim(),
  definition: String(card?.definition || "").trim(),
  example: String(card?.example || "").trim()
});

const parseJsonFromText = (text) => {
  const raw = String(text || "").trim();
  const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)```/i);
  const candidate = fenced ? fenced[1].trim() : raw;
  const start = candidate.indexOf("{");
  const end = candidate.lastIndexOf("}");
  if (start === -1 || end === -1 || end <= start) {
    throw new Error("Gemini response did not contain JSON.");
  }
  return JSON.parse(candidate.slice(start, end + 1));
};

exports.parseMandarinFlashcards = onRequest(
  {
    region: "asia-east1",
    cors: true,
    secrets: [GEMINI_API_KEY],
    timeoutSeconds: 120,
    memory: "512MiB"
  },
  async (req, res) => {
    if (req.method === "OPTIONS") {
      res.status(204).send("");
      return;
    }
    if (req.method !== "POST") {
      res.status(405).json({ error: "Use POST." });
      return;
    }

    try {
      const { imageBase64, mimeType, publisher, book, lessonNo, category } = req.body || {};
      if (!imageBase64 || typeof imageBase64 !== "string") {
        res.status(400).json({ error: "Missing imageBase64." });
        return;
      }

      const ai = new GoogleGenAI({ apiKey: GEMINI_API_KEY.value() });
      const prompt = [
        "你是台灣國小國語課本語詞解釋截圖的結構化整理器。",
        "請直接看圖片，不要做一般 OCR 全文轉錄。",
        "圖片多半是直排中文表格，閱讀順序是由右而左，每欄由上而下。",
        "每一欄通常有三個區塊：上方是詞語或成語，中間是解釋，下方是造句或例句。",
        "注音符號完全忽略，不要輸出注音。",
        "表格標題、欄號、右側的「語詞」「解釋」「造句」標籤都不要輸出。",
        `目前單元資訊：版本=${publisher || ""}，冊別=${book || ""}，課次=${lessonNo || ""}，類型=${category || ""}。`,
        "請只輸出 JSON，不要 Markdown，不要說明文字。",
        "JSON 格式必須是：{\"cards\":[{\"word\":\"\",\"definition\":\"\",\"example\":\"\"}]}",
        "如果某欄辨識不確定，仍盡量填入最可能的中文字；不要輸出亂碼、英文代碼或符號。"
      ].join("\n");

      const response = await ai.models.generateContent({
        model: process.env.GEMINI_MODEL || "gemini-2.0-flash-001",
        contents: [
          {
            role: "user",
            parts: [
              { text: prompt },
              {
                inlineData: {
                  mimeType: mimeType || "image/jpeg",
                  data: imageBase64
                }
              }
            ]
          }
        ]
      });

      const parsed = parseJsonFromText(response.text);
      const cards = Array.isArray(parsed.cards)
        ? parsed.cards.map(normalizeCard).filter((card) => card.word || card.definition || card.example)
        : [];

      res.json({ cards });
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Vision parsing failed." });
    }
  }
);
