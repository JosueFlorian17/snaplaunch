import webbrowser 
urls= [
    "https://mail.google.com/mail/u/0/#inbox",
    "https://www.youtube.com/",
    "https://web.whatsapp.com/",
    "https://x.com/home"
]

new_urls=[]

def add_to_new_order(url):
    if url in new_urls:
        print("Ya has seleccionado esa pestaña")
        add_to_new_order(urls[int(input("Elige otra pestaña\n1. Gmail\n2. Youtube\n3. Whatsapp\n4. X\n"))-1])
    else:
        new_urls.append(url)
        return True

for i in range(0, len(urls)):
    answer = input(f"Elige el orden en que quieres abrir las pestañas\n1. {urls[0]} \n2. {urls[1]} \n3. {urls[2]} \n4. {urls[3]}\n")
    if answer == "1":
        add_to_new_order(urls[0])
    elif answer == "2":
        add_to_new_order(urls[1])
    elif answer == "3":
        add_to_new_order(urls[2])
    elif answer == "4":
        add_to_new_order(urls[3])
    else:
        print("Opción no válida")
        break

print(new_urls)

for url in (new_urls):
    webbrowser.open_new_tab(url)

