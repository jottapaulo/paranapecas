from flask import Flask, request, jsonify
from flask_cors import CORS
from rembg import remove
from PIL import Image
import io, base64

# A Vercel vai procurar por essa variável 'app'
app = Flask(__name__)
# O CORS é importante para permitir que seu index.html acesse a API
CORS(app) 

@app.route("/")
def home():
    # Vercel Serverless Function padrão (acessível em /api/index)
    return jsonify({"status": "API online (Python) 🚀"})

@app.route("/remover-fundo", methods=["POST"])
def remover_fundo():
    # Verifica se há a chave 'imagens' no request.files
    if "imagens" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    imagens = request.files.getlist("imagens")
    resultados = []

    for img in imagens:
        try:
            input_bytes = img.read()
            output_bytes = remove(input_bytes)

            # Converter para PNG base64
            output_image = Image.open(io.BytesIO(output_bytes)).convert("RGBA")
            buffer = io.BytesIO()
            output_image.save(buffer, format="PNG")
            base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            resultados.append(base64_str)
        except Exception as e:
            # Em caso de erro, retorna o erro
            resultados.append(f"erro: {str(e)}")
            # Também loga o erro no console da Vercel
            print(f"Erro ao processar imagem: {str(e)}")

    return jsonify(resultados)
# O bloco if __name__ == "__main__": é removido para Serverless
