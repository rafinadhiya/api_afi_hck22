# Import Libraries
from fastapi import FastAPI, HTTPException, Header
import uvicorn
import pandas as pd

# Bikin instance untuk menangkap REST API (FAST API)
# Setiap kali mau bikin end point harus bikin yg kayak dibawah ini
afi = FastAPI()

# Endpoint utama
@afi.get("/") # Setara dengan 127.0.0.1:8000/ atau localhost:8000/
def home():
    return {"message":"Hello World! This is my first API",
                    "menu":{1:"/students",
                            2:"/horses",
                            3:"shopping_cart"}}
    
#########################################Load From JSON#########################################

students_data = {
    "Joni":{
        "shoe_size":44,
        "fav_color":"Black"
    },
    "Salsa":{
        "shoe_size":39,
        "fav_color":"white"
    },
    "Dewa":{
        "shoe_size":42,
        "fav_color":"blue"       
    }
}

# Endpoint students
@afi.get("/students")
def students():
    return {"message":"Ini merupakan API untuk menampilkan, menambah, dan menghapus data siswa",
            "menu":{
                1:"/data",
                2:"/find_student/{name}",
                3:"/add_student",
                4:"/update_student/{name}",
                5:"/delete_student/{name}"
            }}

# Endpoint menampilkan semua data
@afi.get("/students/data")
def std_data():
    return students_data

# Endpoint mencari siswa 
@afi.get("/students/find_student/{name}")
def find_student(name:str):
    # Conditional pengecekan apakah nama siswa ada
    if name in students_data.keys():
        return {name:students_data[name]}
    else:
        raise HTTPException(status_code=404, detail="Students not found!")
    
# Endpoint menambah data siswa 
@afi.post("/students/add_student")
def add_std(student_data:dict):
    # Untuk menambahkan print pesan dalam terminal
    print(f"Student Data: {student_data}")
    # Untuk menangkap masukan user
    student_name = student_data["name"]
    student_shoe_size = student_data["shoe_size"]
    student_fav_color = student_data["fav_color"]
    # Untuk menambahkan data dalam dictionary
    students_data[student_name] = {
        "shoe_size":student_shoe_size,
        "fav_color":student_fav_color
    }
    # Untuk menambahkan pesan dalam tampilan API
    return{"message":f"Student {student_name} successfully added!"}

# Endpoint untuk update/edit data
@afi.put("/students/update_student{name}")
def put_std(name:str, student_data:dict):
    # Conditional pengecekan apakah nama ada dalam data
    if name not in students_data.keys():
        raise HTTPException(status_code=404, detail=f"Student {name} not found!")
    else:
        # Assign variabel value dari hasil slicing dictionary students_data dalam student_data
        students_data[name] = student_data
        # Menampilkan pesan dalam API
        return {"message":f"Students {name} has been updated!"}
    
# Endpoint untuk hapus data siswa
@afi.delete("/students/delete_student/{name}")
def del_std(name:str):
    if name in students_data.keys():
        # Hapus data siswa berdasarkan hasil slicing dictionary
        del students_data[name]
        return {"message":f"Student data {name} has been deleted"}
    else:
        raise HTTPException(status_code=404, detail=f"Student {name} not found!")

    
#########################################Load From CSV#########################################
# Load data disimpan dalam variabel 'horse'
horse = pd.read_csv("horse_clean.csv")

# Endpoint horse home
@afi.get("/horses")
def kandang():
    return{"message":"Selamat datang di sub-menu perkudaan hewan paling keren!",
            "menu":{
                1:"Get all horses (/horses/data)",
                2:"Filter by surgery (/horses/surgery/{surg})",
                4:"Filter by outcome (/horses/outcome/{out})",
                5:"Delete horses data by Unnamed: 0 *Sad :'( (/horses/del/{id})"
    }}

# Endpoint show horses data
@afi.get("/horses/data")
def kuda():
    return horse.to_dict(orient = "records")

# Endpoint filter by surgery
@afi.get("/horses/surgery/{surgery_type}")
def operasi(surgery_type:str):
    # Mennyimpan hasil slicing dalam variabel baru
    horse_surgery = horse[horse["surgery"]==surgery_type]
    # Return hasil slicing
    return horse_surgery.to_dict(orient="records")

# Endpoint filter by outcome
@afi.get("/horses/outcome/{outcome_type}")
def idup(outcome_type:str):
    # Menyimpan hasil slicing dalam variabel baru
    horse_outcome = horse[horse["outcome"]==outcome_type]
    # Return hasil slicing
    return horse_outcome.to_dict(orient="records")

# API KEY (Password)
API_KEY = "admin1234"

# Endpoint untuk hapus data menggunakan akses API Key
@afi.delete("/horses/del/{id}")
def apus(id:int, api_key:str=Header(None)): # Memasang API Key dalam Header dengan default value None
    # Menunjukkan value api_key dalam terminal
    print(api_key)
    # Conditional pengecekan API Key
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API Key masih kosong atau salah")
    # Kalo API Key bener
    else:
        # Pengecekan apakah id ada dalam kolom unnamed: 0
        if id not in horse["Unnamed: 0"].values:
            raise HTTPException(status_code=404, detail=f"Horse with id {id} did not found!")
        # Kalo ketemu / ada
        else: 
            horse.drop(horse[horse["Unnamed: 0"]==id].index, inplace=True)
            return {"message":f"Horse with id {id} succesfully deleted!"}
        

#########################################Shopping Cart########################################


cart = {"name": "shopping cart",
        "columns": ["prod_name", "price", "num_items"],
        "items": {}}


@afi.get("/shopping_cart")
def root():
    return {"message": "Welcome to Toko H8 Shopping Cart! There are some features that you can explore",
            "menu": {1: "See shopping cart (/shopping_cart/cart)",
                     2: "Add item (/shopping_cart/add)",
                     3: "Edit shopping cart (/shopping_cart/edit/{id})",
                     4: "Delete item from shopping cart (/shopping_cart/del/{id})",
                     5: "Calculate total price (/shopping_cart/total)",
                     6: "Exit (/shopping_cart/exit)"}
            }


@afi.get("/shopping_cart/cart")
def show():
    return cart


@afi.post("/shopping_cart/add")
def add_item(added_item: dict):
    id = len(cart["items"].keys()) + 1
    cart["items"][id] = added_item
    return f"Item successfully added into your cart with ID {id}"


@afi.put("/shopping_cart/edit/{id}")
def update_cart(id: int, updated_cart: dict):
    if id not in cart['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        cart["items"][id].update(updated_cart)
        return {"message": f"Item with ID {id} has been updated successfully."}


@afi.delete("/shopping_cart/del/{id}")
def remove_row(id: int):
    if id not in cart['items'].keys():
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    else:
        cart["items"].pop(id)
        return {"message": f"Item with ID {id} has been deleted successfully."}


@afi.get("/shopping_cart/total")
def get_total():
    total_price = sum(item["price"] * item["num_items"] for item in cart["items"].values())
    return {"total_price": total_price}


@afi.get("/shopping_cart/exit")
def exit():
    return {"message": "Thank you for using Toko H8 Shopping Cart! See you next time."}

# Biar langsung dijalankan 
if __name__ == "__main__":
    uvicorn.run("hck22_api_afi:afi", host="127.0.0.1", port=8000, reload=True)