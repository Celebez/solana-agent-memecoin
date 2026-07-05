name: "Security Report"
description: "🔒 Laporkan kerentanan keamanan (PRIVATE)"
title: "[SECURITY] "
labels: ["security", "priority: high"]
assignees: []
body:
  - type: markdown
    attributes:
      value: |
        ⚠️ **Untuk kerentanan sensitif, jangan gunakan issue ini.**
        Email langsung ke maintainer.

  - type: textarea
    id: deskripsi
    attributes:
      label: Deskripsi Kerentanan
    validations:
      required: true

  - type: textarea
    id: dampak
    attributes:
      label: Dampak Potensial
    validations:
      required: true

  - type: textarea
    id: reproduksi
    attributes:
      label: Langkah Reproduksi
    validations:
      required: true
