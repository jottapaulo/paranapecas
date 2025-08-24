from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io, base64, os

# Inicializa o app Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS (permite requisições do frontend)

@app.route('/remover-fundo', methods=['POST'])
def remover_fundo():
    # Recebe múltiplas imagens do campo "imagens"
    files = request.files.getlist('imagens')  
    if not files:
        return {"erro": "Envie pelo menos uma imagem com o campo 'imagens'."}, 400

    resultados = []

    for file in files:
        input_image = file.read()

        # Remove fundo com rembg
        output_image = remove(input_image)

        # Converte para PNG com transparência
        img = Image.open(io.BytesIO(output_image)).convert("RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        # Converte imagem para base64
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        resultados.append(img_base64)

    # Retorna lista de imagens em base64
    return jsonify(resultados)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render usa a PORT, default 10000
    app.run(host="0.0.0.0", port=port)
