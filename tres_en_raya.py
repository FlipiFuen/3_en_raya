import tkinter as tk

from interfaz import TITULO, Ventana

def main():
    raiz = tk.Tk()
    raiz.title(TITULO)
    raiz.geometry("800x800")
    app = Ventana(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    main()