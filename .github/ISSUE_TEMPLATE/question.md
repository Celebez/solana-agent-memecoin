name: "Pertanyaan / Diskusi"
description: "Pertanyaan umum, klarifikasi, atau diskusi"
title: "[Q] "
labels: ["question"]
assignees: []
body:
  - type: markdown
    attributes:
      value: Sebelum bertanya, pastikan sudah cek [Docs](../../tree/main/docs) dan [Issues sebelumnya](../../issues?q=is%3Aissue).

  - type: textarea
    id: pertanyaan
    attributes:
      label: Pertanyaan Anda
    validations:
      required: true

  - type: textarea
    id: riset
    attributes:
      label: Apa yang sudah Anda coba?
    validations:
      required: false
