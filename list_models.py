import google.generativeai as genai

genai.configure(api_key="AIzaSyBVrMrPz4yff7MIVPij0q7hGkR80rrNl84")

models = genai.list_models()

for m in models:
    print(m.name, "→", m.supported_generation_methods)
