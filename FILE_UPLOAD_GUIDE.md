# File Upload Implementation Guide - Menu Photo

## Ringkasan Perubahan

Implementasi file upload untuk kolom foto di menu telah selesai. Berikut adalah penjelasan lengkapnya.

## 1. Perubahan di Backend

### A. Model (menu_model.py)
- Ditambahkan `MenuCreateWithFile` model untuk handle file upload
- Model ini digunakan khusus untuk endpoint upload dengan form data

### B. Service (menu_service.py)
Ditambahkan 2 fungsi baru:

**1. `save_upload_file()`**
- Menyimpan file ke folder `uploads/menu/`
- Validasi format file (hanya .jpg, .jpeg, .png, .gif, .webp)
- Menambahkan timestamp untuk unique filename
- Return: nama file yang disimpan

**2. `create_menu_with_file()`**
- Membuat menu baru dengan file upload
- Memanggil `save_upload_file()` untuk handle file
- Menyimpan nama file ke kolom `foto` di database

### C. Routes (menu_routes.py)
Ditambahkan endpoint baru:

```
POST /menus/upload
```

**Request Format (multipart/form-data):**
```
- nama_menu: string (required)
- kategori: integer (required)
- harga: float (required)
- stok: integer (required)
- foto: file (optional)
```

**Example dengan curl:**
```bash
curl -X POST "http://localhost:8000/menus/upload" \
  -H "accept: application/json" \
  -F "nama_menu=Nasi Goreng" \
  -F "kategori=1" \
  -F "harga=25000" \
  -F "stok=50" \
  -F "foto=@/path/to/image.jpg"
```

### D. Main Application (main.py)
- Ditambahkan mount untuk static files di path `/uploads`
- Auto-create folder `uploads/` jika belum ada
- File yang diupload dapat diakses via `http://localhost:8000/uploads/menu/FILENAME`

---

## 2. Struktur Folder

```
resto/
├── uploads/
│   └── menu/
│       ├── 20260202_143022_nasi_goreng.jpg
│       ├── 20260202_143045_soto_ayam.png
│       └── ...
├── app/
├── alembic/
├── main.py
└── ...
```

---

## 3. Cara Menggunakan di Frontend

### Option A: HTML Form Upload
```html
<form id="menuForm" enctype="multipart/form-data">
  <input type="text" name="nama_menu" placeholder="Nama Menu" required>
  <input type="number" name="kategori" placeholder="Kategori ID" required>
  <input type="number" step="0.01" name="harga" placeholder="Harga" required>
  <input type="number" name="stok" placeholder="Stok" required>
  <input type="file" name="foto" accept="image/*">
  <button type="submit">Tambah Menu</button>
</form>

<script>
document.getElementById('menuForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(e.target);
  
  try {
    const response = await fetch('http://localhost:8000/menus/upload', {
      method: 'POST',
      body: formData
    });
    
    const data = await response.json();
    console.log('Menu created:', data);
    alert('Menu berhasil ditambahkan!');
  } catch (error) {
    console.error('Error:', error);
    alert('Error menambahkan menu');
  }
});
</script>
```

### Option B: JavaScript (Fetch API)
```javascript
async function uploadMenu(nama_menu, kategori, harga, stok, fotoFile) {
  const formData = new FormData();
  formData.append('nama_menu', nama_menu);
  formData.append('kategori', kategori);
  formData.append('harga', harga);
  formData.append('stok', stok);
  
  if (fotoFile) {
    formData.append('foto', fotoFile);
  }
  
  const response = await fetch('http://localhost:8000/menus/upload', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// Usage
const fileInput = document.getElementById('fotoInput');
uploadMenu('Nasi Goreng', 1, 25000, 50, fileInput.files[0]);
```

### Option C: React
```jsx
import { useState } from 'react';

function MenuUpload() {
  const [formData, setFormData] = useState({
    nama_menu: '',
    kategori: '',
    harga: '',
    stok: '',
    foto: null
  });

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'foto') {
      setFormData(prev => ({ ...prev, foto: files[0] }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const data = new FormData();
    data.append('nama_menu', formData.nama_menu);
    data.append('kategori', formData.kategori);
    data.append('harga', formData.harga);
    data.append('stok', formData.stok);
    if (formData.foto) {
      data.append('foto', formData.foto);
    }
    
    try {
      const response = await fetch('http://localhost:8000/menus/upload', {
        method: 'POST',
        body: data
      });
      const result = await response.json();
      console.log('Menu created:', result);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input 
        type="text" 
        name="nama_menu"
        value={formData.nama_menu}
        onChange={handleChange}
        placeholder="Nama Menu"
        required
      />
      <input 
        type="number" 
        name="kategori"
        value={formData.kategori}
        onChange={handleChange}
        placeholder="Kategori ID"
        required
      />
      <input 
        type="number" 
        step="0.01"
        name="harga"
        value={formData.harga}
        onChange={handleChange}
        placeholder="Harga"
        required
      />
      <input 
        type="number" 
        name="stok"
        value={formData.stok}
        onChange={handleChange}
        placeholder="Stok"
        required
      />
      <input 
        type="file" 
        name="foto"
        onChange={handleChange}
        accept="image/*"
      />
      <button type="submit">Tambah Menu</button>
    </form>
  );
}

export default MenuUpload;
```

---

## 4. Response dari API

**Success (201 Created):**
```json
{
  "id": 5,
  "nama_menu": "Nasi Goreng",
  "kategori": 1,
  "harga": 25000,
  "stok": 50,
  "model_config": {}
}
```

**Error (400 Bad Request):**
```json
{
  "detail": "File type .pdf is not allowed. Allowed types: {'.jpg', '.jpeg', '.png', '.gif', '.webp'}"
}
```

---

## 5. Mengakses File Foto

Setelah upload berhasil, foto dapat diakses di:

```
http://localhost:8000/uploads/menu/{filename}
```

**Contoh:**
```
http://localhost:8000/uploads/menu/20260202_143022_nasi_goreng.jpg
```

Gunakan URL ini di frontend untuk menampilkan gambar:
```html
<img src="http://localhost:8000/uploads/menu/20260202_143022_nasi_goreng.jpg" alt="Nasi Goreng">
```

---

## 6. Validasi File

File yang diizinkan:
- `.jpg` / `.jpeg`
- `.png`
- `.gif`
- `.webp`

Jika format file tidak sesuai, akan menerima error 400.

---

## 7. Notes Penting

1. **Upload tanpa foto:** Foto bersifat optional. Anda bisa submit form tanpa foto.

2. **Unique filename:** Setiap file diberi timestamp untuk memastikan tidak ada nama duplikat.

3. **Database:** Kolom `foto` di tabel `menu` menyimpan nama file, bukan full path.

4. **Update menu dengan foto baru:** Saat ini belum ada endpoint untuk update foto. Jika perlu, tambahkan fungsi update di service.

---

## 8. Troubleshooting

**Problem: "uploads folder not found"**
- Solution: Folder akan auto-create saat startup. Jika masih error, buat folder `uploads/menu/` manually.

**Problem: "Permission denied"**
- Solution: Pastikan aplikasi punya permission untuk write ke folder `uploads/`.

**Problem: File tidak muncul di response**
- Solution: Cek di database apakah kolom `foto` berisi nama file. Jika tidak, cek console untuk error.
