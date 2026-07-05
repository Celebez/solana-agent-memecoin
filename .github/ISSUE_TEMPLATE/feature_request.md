name: "Feature Request"
description: "Usulkan konten, script, atau section baru"
title: "[FEAT] "
labels: ["enhancement"]
assignees: []
body:
  - type: markdown
    attributes:
      value: Mau repo ini lebih lengkap? Ajukan ide Anda! 💡

  - type: textarea
    id: masalah
    attributes:
      label: Masalah yang Ingin Dipecahkan
      placeholder: Saya kesulitan mencari info tentang...
    validations:
      required: true

  - type: textarea
    id: solusi
    attributes:
      label: Solusi yang Diusulkan
      placeholder: Tambahkan section tentang...
    validations:
      required: true

  - type: textarea
    id: alternatif
    attributes:
      label: Alternatif yang Sudah Dicoba
    validations:
      required: false

  - type: textarea
    id: konteks
    attributes:
      label: Konteks Tambahan
      placeholder: Target pengguna, benefit, dll.
    validations:
      required: false
