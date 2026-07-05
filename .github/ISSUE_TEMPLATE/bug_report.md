name: "Bug Report"
description: "Laporkan bug atau error di panduan/script"
title: "[BUG] "
labels: ["bug", "triage"]
assignees: []
body:
  - type: markdown
    attributes:
      value: Terima kasih sudah meluangkan waktu melaporkan bug! 🙏

  - type: dropdown
    id: severity
    attributes:
      label: Tingkat Keparahan
      description: Seberapa serius masalah ini?
      options:
        - 🔴 Kritis (kehilangan dana, kerentanan keamanan)
        - 🟠 Tinggi (script tidak jalan, info salah)
        - 🟡 Sedang (typo, link rusak)
        - 🟢 Rendah (saran perbaikan)
    validations:
      required: true

  - type: textarea
    id: deskripsi
    attributes:
      label: Deskripsi Masalah
      placeholder: Jelaskan apa yang terjadi...
    validations:
      required: true

  - type: textarea
    id: reproduksi
    attributes:
      label: Langkah Reproduksi
      placeholder: |
        1. Jalankan command '...'
        2. Dengan input '...'
        3. Lihat error '...'
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Perilaku yang Diharapkan
    validations:
      required: false

  - type: textarea
    id: lingkungan
    attributes:
      label: Lingkungan
      placeholder: |
        - OS: [mis. Ubuntu 22.04]
        - Python: [mis. 3.11]
        - Branch: [mis. main]
    validations:
      required: false
