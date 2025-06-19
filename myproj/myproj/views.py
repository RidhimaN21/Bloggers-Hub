from django.shortcuts import render
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def homepage(request):
    response = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.POST.get("user_message", "")
        if user_message:
            input_ids = tokenizer.encode(user_message, return_tensors="pt")

            with torch.no_grad():
                output_ids = model.generate(
                    input_ids,
                    max_length=100,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2,
                    do_sample=True,
                    top_k=50,
                    top_p=0.95,
                    temperature=0.9,
                )
            
            response = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return render(request, "home.html", {
        "response": response,
        "user_message": user_message
    })
