from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Fungsi untuk memprediksi
def predict(menirukan, frekuensi, emosi, tercerminkan, mindset, 
            sumber_inspirasi, tindakan_positif, cara_komunikasi):
    # Contoh penggunaan model Naive Bayes (sesuaikan dengan struktur data Anda)
    gaussian = GaussianNB()
    gaussian.fit(X_train, y_train)

    # Transformasi nilai input menjadi array
    input_data = [
        menirukan,
        frekuensi,
        emosi,
        tercerminkan,
        mindset,
        sumber_inspirasi,
        tindakan_positif,
        cara_komunikasi
    ]

    Y_pred = gaussian.predict([input_data])

    return int(Y_pred[0])

@app.route('/predict', methods=['POST'])
def prediction_endpoint():
    # Ambil data dari formulir JSON
    data = request.get_json()

    menirukan = int(data["menirukan"])
    frekuensi = int(data["frekuensi"])
    emosi = int(data["emosi"])
    tercerminkan = int(data["tercerminkan"])
    mindset = int(data["mindset"])
    sumber_inspirasi = int(data["sumber_inspirasi"])
    tindakan_positif = int(data["tindakan_positif"])
    cara_komunikasi = int(data["cara_komunikasi"])

    # Contoh penggunaan model pada data yang baru
    prediction = predict(menirukan, frekuensi, emosi, tercerminkan, mindset,
                         sumber_inspirasi, tindakan_positif, cara_komunikasi)

    # Konversi nilai prediksi ke pesan yang diinginkan
    prediction_message = "Ya, Terdapat Perubahan Dalam Perilaku Sehari-hari Setelah Menonton Drama" if prediction == 1 else "Tidak ada Perubahan Dalam Perilaku Sehari-hari Setelah Menonton Drama"

    # Mengirimkan hasil prediksi sebagai respon JSON
    response_data = {"prediction": int(prediction), "prediction_message": prediction_message}
    return jsonify(response_data)

# Route for serving the index.html file
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Load data atau sesuaikan dengan kebutuhan
    df = pd.read_excel('Kuesioner.xlsx')

    # Transformasi label menggunakan LabelEncoder
    labelencoder = LabelEncoder()

    df['Menirukan'] = labelencoder.fit_transform(df['Menirukan'])  # Ya = 1, Tidak = 0

    label_columns = [
        'Frekuensi',  # 1-5 kali = 1, 6-10 kali = 2, Lebih dari 10 kali = 3
        'Emosi',  # Sering = 1, Tidak = 2, Ya = 3
        'Tercerminkan',  # Mungkin = 1, Tidak = 2, Ya = 3
        'Mindset'  # Sering = 1, Tidak = 2, Ya = 3
    ]
    for column in label_columns:
        df[column] = labelencoder.fit_transform(df[column]) + 1

    df['Perubahan'] = labelencoder.fit_transform(df['Perubahan'])  # Ya = 1, Tidak = 0

    X = df.iloc[:, 0:8].values
    y = df.iloc[:, 8].values

    # Split data menjadi data latih dan data uji
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.1, random_state=42)

    app.run(debug=True)
