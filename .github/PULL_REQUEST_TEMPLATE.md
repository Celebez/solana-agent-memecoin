name: Pull Request
description: "Kontribusi kode/dokumentasi"
body:
  - type: markdown
    attributes:
      value: |
        Terima kasih sudah berkontribusi! 🙏
        Pastikan sudah baca [CONTRIBUTING.md](../../blob/main/CONTRIBUTING.md).

  - type: dropdown
    id: jenis
    attributes:
      label: Jenis Perubahan
      options:
        - 🐛 Bug fix
        - ✨ Fitur baru
        - 📚 Dokumentasi
        - 🎨 Perbaikan gaya/format
        - ⚡ Performance
        - 🔒 Security fix
        - 🧪 Test
    validations:
      required: true

  - type: textarea
    id: deskripsi
    attributes:
      label: Deskripsi Perubahan
    validations:
      required: true

  - type: textarea
    id: testing
    attributes:
      label: Cara Testing
    validations:
      required: true

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: Kode/script sudah saya test secara lokal
        - label: Saya tidak commit private key / seed / API key
        - label: Saya update dokumentasi terkait
        - label: Perubahan mengikuti gaya repo
