from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io, base64

app = Flask(__name__)
CORS(app)  # permite acesso do seu site

@app.route("/")
def home():
    return jsonify({"status": "API online 🚀"})

@app.route("/remover-fundo", methods=["POST"])
def remover_fundo():
    if "imagens" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    imagens = request.files.getlist("imagens")
    resultados = []

    for img in imagens:
        try:
            input_bytes = img.read()
            output_bytes = remove(input_bytes)

            # converter para PNG base64
            output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
            buffer = io.BytesIO()
            output_image.save(buffer, format="PNG")
            base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            resultados.append(base64_str)
        except Exception as e:
            resultados.append(f"erro: {str(e)}")

    return jsonify(resultados)

if __name__ == "__main__":
    # Render exige usar host 0.0.0.0 e porta vinda do ambiente
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
