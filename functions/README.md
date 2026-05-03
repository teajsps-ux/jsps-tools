# Mandarin Flashcard Vision Function

This Firebase Function keeps the Gemini API key on the server and returns
structured flashcard data for the Mandarin flashcard tool.

## Setup

Do not put API keys in HTML files.

Firebase Functions deployment requires the Firebase project to be on the Blaze
pay-as-you-go plan because Cloud Build and Artifact Registry are required.

Set the Gemini key as a Firebase Secret:

```powershell
npx.cmd firebase-tools functions:secrets:set GEMINI_API_KEY --project jsps-tools-sync
```

Deploy only this function:

```powershell
npx.cmd firebase-tools deploy --only functions:parseMandarinFlashcards --project jsps-tools-sync
```

The default frontend endpoint is:

```text
https://asia-east1-jsps-tools-sync.cloudfunctions.net/parseMandarinFlashcards
```

If the deployed URL differs, copy the function URL and paste it into the web tool via:

`編輯單元 -> 設定 Gemini / Claude Vision 後端`

## Local Note

Avoid running `npm install` inside the Google Drive synced folder if it causes
`EBADF` or `EPERM` errors. Firebase installs dependencies from `package.json`
during deployment.
