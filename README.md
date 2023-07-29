# seleksi-labpro-monolith

## Identitas diri

**Nama:** Rinaldy Adin
<br>
**NIM:** 13521134

## Cara menjalankan

## Design Pattern yang digunakan

### 1. Chain of Responsibility

Chain of Responsibility adalah design pattern behaioral yang memungkinkan adanya penanganan request secara sekuaensial melalui berbagai handler dengan perilaku yang berbeda. Setiap handler dalam rantai memutuskan apakah dia dapat menangani permintaan tersebut. Jika dia bisa menanganinya, maka dia akan menanganinya; jika tidak, maka permintaan tersebut akan diteruskan ke handler berikutnya dalam rantai. Pengirim permintaan tidak perlu tahu struktur internal dari rantai objek penangan, sehingga memungkinkan penanganan yang dinamis dan terpisah.

Pada program monolith saya, design pattern Chain of Responsibility dimanfaatkan pada penggunaan middleware yang digunakan untuk melakukan otentikasi pengguna menggunakan JWT.

```py
class JWTAuthMiddleware:
    ...

    def __call__(self, request: HttpRequest):
        excluded_paths = [
            reverse("users:login"),
            reverse("users:register"),
        ]

        if request.path.startswith("/admin/") or request.path == "/admin":
            response = self.get_response(request)
            return response

        if "AUTH_TOKEN" not in request.COOKIES and request.path in excluded_paths:
            response = self.get_response(request)
            return response

        token = request.COOKIES.get("AUTH_TOKEN")
        secret_key = os.environ.get("SECRET_KEY")

        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return redirect(reverse("users:login"), status=401)
        except jwt.InvalidTokenError:
            return redirect(reverse("users:login"), status=401)

        if request.path in excluded_paths:
            return redirect(reverse("users:catalog"))

        request.user = {"username": decoded_token["username"]}

        response = self.get_response(request)
        return response
```

Pada snippet program di atas, middleware/handler JWTAuthMiddleware bisa menentukan untuk melanjutkan rantai pemanggilan handler pada bagian `return response` , atau bisa menghentikan rantai pemanggilan dengan melakukan redirect seperti `return redirect(reverse("users:catalog"))`

### 2. Proxy Pattern

Proxy Pattern adalah structural design pattern yang digunakan untuk mengontrol akses ke objek lain dengan menambahkan objek perantara di antara klien dan objek yang sebenarnya. Tujuan utama dari pola ini adalah untuk menyediakan wadah pengganti yang dapat mengontrol atau menambahkan fungsi tambahan saat klien berinteraksi dengan objek asli tanpa perlu mengubah kode klien. Pada program ini, proxy pattern digunakan pada implementasi query yang dilakukan terhadap basis data karena dilakukan melalui sebuah ORM yang diimplementasi oleh Django.

```py
user = User.objects.get(username=request.POST["username"])
```

Pada snippet program di atas, dilakukan query terhadap basis data terhadap tabel User untuk mendapatkan salah satu record berdasarkan username. Pada contoh diatas, pengambilan data dari basis data tidak dilakukan secara langsung terhadap basis data, tetapi melalui ORM, yang bertindak sebagai proxy, terlebih dahulu.

### 3. Template Method

Template Method (Metode Template) adalah behavioral design pattern yang digunakan untuk mengatur alur atau urutan operasi dalam sebuah metode, tetapi mengizinkan implementasi rinci dari langkah-langkah tersebut ditentukan/dimodifikasi oleh subclass. Dengan pola ini, kita dapat menentukan kerangka umum atau algoritma dasar dalam metode utama, sementara detail implementasi langkah-langkahnya ditangani oleh kelas-kelas turunannya. Penggunaan template method dalam program ini ada pada penggunaan Generic Views.

```py
class HistoryListView(ListView):
    template_name = "history.html"
    model = History
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        return History.objects.filter(username__username=self.request.user["username"])

    ...
```

Pada implementasi `HistoryListView` di atas, yang merupakan subclass dari `ListView`, dilakukan implementasi lebih rinci dalam fungsi `get_queryset` yang melakukan filter lebih rinci terhadap record-record `History` yang akan ditampilkan, agar hanya menampilkan `History` dari pengguna saat itu saja. Program sebenarnya akan tetap jalan dengan normal ketika fungsi `get_queryset` tidak terdefinisi, tetapi implementasi yang terjadi adalah semua record `History` yang ada akan ditampilkan juga pada `ListView` tersebut

## Technology Stack

**Bahasa:** Python (3.10)<br>
**Framework**: Django (4.2)<br>
**Package Lainnya:**<br>

```
# requirements.txt
Django==4.2.3
PyJWT==2.8.0
PyJWT==2.8.0
python-dotenv==1.0.0
python_bcrypt==0.3.2
Requests==2.31.0
```

## Endpoints

**login :** Halaman login
<br>
**logout :** Endpoint logout
<br>
**register :** Halaman register (membuat akun baru)
<br>
**catalog :** Halaman katalog barang
<br>
**history :** Halaman riwayat pembelian
<br>
**detail/:id :** Halaman detail barang
<br>
**buy/:id :** Halaman beli barang
<br>
**admin/ :** Halaman admin Django (bawaan Django)

## Bonus

-   Tidak ada pada monolith
