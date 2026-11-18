MODE_BADGE = "PURE PYTHON"
def transpose(a):
    return [[a[r][c] for r in range(3)] for c in range(3)]
def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
          - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
          + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
def inverse(a):
    d = determinant(a)
    if abs(d) < 1e-10:
        raise ValueError("This matrix has no inverse because its determinant is zero.")
    cof = []
    for r in range(3):
        row = []
        for c in range(3):
            minor = [[a[i][j] for j in range(3) if j != c]
                     for i in range(3) if i != r]
            md = minor[0][0]*minor[1][1] - minor[0][1]*minor[1][0]
            row.append(((-1)**(r+c))*md)
        cof.append(row)
    adj = transpose(cof)
    return [[adj[r][c]/d for c in range(3)] for r in range(3)]
def calculate(op, a, b=None, scalar=1):
    if op == "Addition": return [[a[r][c]+b[r][c] for c in range(3)] for r in range(3)]
    if op == "Subtraction": return [[a[r][c]-b[r][c] for c in range(3)] for r in range(3)]
    if op == "Matrix Multiplication":
        return [[sum(a[r][k]*b[k][c] for k in range(3)) for c in range(3)] for r in range(3)]
    if op == "Element-wise Multiplication": return [[a[r][c]*b[r][c] for c in range(3)] for r in range(3)]
    if op == "Transpose (A)": return transpose(a)
    if op == "Determinant (A)": return [[determinant(a)]]
    if op == "Inverse (A)": return inverse(a)
    if op == "Scalar Multiplication (A)": return [[a[r][c]*scalar for c in range(3)] for r in range(3)]
    if op == "Trace (A)": return [[a[0][0]+a[1][1]+a[2][2]]]
    raise ValueError("Unknown operation.")

import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import sys

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# A completely different warm-luxe palette: deep teal, pearl, champagne and coral.
BG = "#0B3438"
BG_MID = "#10464A"
PEARL = "#F7F5EF"
WHITE = "#FFFEFA"
INK = "#183638"
MUTED = "#718487"
TEAL = "#167C80"
TEAL_HOVER = "#0F666B"
MINT = "#DDF1E9"
CHAMPAGNE = "#D9BD83"
CORAL = "#D87968"
LINE = "#E4E9E3"
PALE = "#EFF4F0"
RESULT = "#123D40"

OPERATIONS = [
    "Addition", "Subtraction", "Matrix Multiplication",
    "Element-wise Multiplication", "Transpose (A)", "Determinant (A)",
    "Inverse (A)", "Scalar Multiplication (A)", "Trace (A)"
]
TWO_MATRIX = {"Addition", "Subtraction", "Matrix Multiplication", "Element-wise Multiplication"}

def fmt(m):
    return "\n".join("     ".join(f"{x:>10.4g}" for x in row) for row in m)

def cmd():
    print("\nMATRIXLAB LUXE | 3 x 3 MATRIX OPERATIONS")
    def getmat(label):
        rows=[]
        print(f"Enter Matrix {label}:")
        for i in range(3):
            while True:
                try:
                    row=[float(x) for x in input(f"Row {i+1} (3 values): ").split()]
                    if len(row)!=3: raise ValueError
                    rows.append(row); break
                except ValueError: print("Please enter exactly 3 valid numbers.")
        return rows
    a=getmat("A")
    for i,x in enumerate(OPERATIONS,1): print(f"{i}. {x}")
    while True:
        try:
            n=int(input("Choose operation (1-9): "))
            if 1<=n<=9: break
        except ValueError: pass
        print("Choose a number from 1 to 9.")
    op=OPERATIONS[n-1]
    b=getmat("B") if op in TWO_MATRIX else None
    scalar=float(input("Scalar value: ")) if op=="Scalar Multiplication (A)" else 1
    try: print("\nRESULT\n"+fmt(calculate(op,a,b,scalar)))
    except Exception as e: print("Error:",e)

class App:
    def __init__(self, root):
        self.root=root
        root.title("MatrixLab Luxe | Matrix Workspace")
        root.geometry("1160x640")
        root.minsize(900,600)
        root.configure(fg_color=BG)
        self.cells={}
        self.build()

    def build(self):
        # Left navigation rail
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        rail=ctk.CTkFrame(self.root, width=205, corner_radius=0, fg_color="#082B2F")
        rail.grid(row=0,column=0,sticky="nsew")
        rail.grid_propagate(False)
        ctk.CTkLabel(rail,text="M.",font=("Georgia",34,"bold"),text_color=CHAMPAGNE).pack(anchor="w",padx=25,pady=(30,0))
        ctk.CTkLabel(rail,text="MATRIXLAB",font=("Arial",13,"bold"),text_color=WHITE).pack(anchor="w",padx=27,pady=(0,2))
        ctk.CTkLabel(rail,text="L U X E   E D I T I O N",font=("Arial",8,"bold"),text_color="#91B7B2").pack(anchor="w",padx=27,pady=(0,42))
        ctk.CTkLabel(rail,text="WORKSPACE",font=("Arial",9,"bold"),text_color="#7EA6A2").pack(anchor="w",padx=24,pady=(0,12))
        for symbol,label,active in [("▦","Matrix studio",True),("ƒ","Operations",False),("◈","Result history",False)]:
            f=ctk.CTkFrame(rail,fg_color="#155357" if active else "transparent",corner_radius=10)
            f.pack(fill="x",padx=13,pady=4)
            ctk.CTkLabel(f,text=symbol,font=("Arial",16),text_color=CHAMPAGNE if active else "#8EAFAB",width=30).pack(side="left",padx=(10,2),pady=10)
            ctk.CTkLabel(f,text=label,font=("Arial",11,"bold" if active else "normal"),text_color=WHITE if active else "#A9C1BE").pack(side="left")
        ctk.CTkFrame(rail,fg_color="#28585A",height=1).pack(fill="x",padx=22,pady=(34,18))
        ctk.CTkLabel(rail,text="SUPPORTED MODE",font=("Arial",8,"bold"),text_color="#7EA6A2").pack(anchor="w",padx=24)
        ctk.CTkLabel(rail,text=MODE_BADGE,font=("Arial",10,"bold"),text_color=CHAMPAGNE,wraplength=155,justify="left").pack(anchor="w",padx=24,pady=8)
        ctk.CTkLabel(rail,text="3 × 3  •  NINE OPERATIONS",font=("Arial",8),text_color="#7EA6A2").pack(side="bottom",pady=22)

        main=ctk.CTkFrame(self.root,fg_color=BG)
        main.grid(row=0,column=1,sticky="nsew",padx=25,pady=12)
        main.grid_columnconfigure((0,1),weight=1)
        main.grid_rowconfigure(4,weight=1, minsize=170)

        top=ctk.CTkFrame(main,fg_color="transparent")
        top.grid(row=0,column=0,columnspan=2,sticky="ew",pady=(0,9))
        ctk.CTkLabel(top,text="Matrix workspace",font=("Georgia",27,"bold"),text_color=WHITE).pack(anchor="w")
        ctk.CTkLabel(top,text="A considered space for clear, accurate matrix calculations.",
                     font=("Arial",11),text_color="#A9C7C1").pack(anchor="w",pady=(5,0))
        ctk.CTkLabel(top,text="✦  PRECISION • SIMPLICITY • ELEGANCE",
                     font=("Arial",9,"bold"),text_color=CHAMPAGNE).pack(anchor="e",pady=(0,4))

        self.matrix_card(main,"A","PRIMARY MATRIX",0,[[1,2,3],[4,5,6],[7,8,9]])
        self.matrix_card(main,"B","SECOND MATRIX",1,[[9,8,7],[6,5,4],[3,2,1]])

        control=ctk.CTkFrame(main,fg_color=PEARL,corner_radius=18,border_width=1,border_color="#D8E2DA")
        control.grid(row=2,column=0,columnspan=2,sticky="ew",pady=9)
        ctk.CTkLabel(control,text="CALCULATION SETTINGS",font=("Arial",9,"bold"),text_color=TEAL).grid(row=0,column=0,columnspan=5,sticky="w",padx=20,pady=(9,4))
        self.op=ctk.StringVar(value=OPERATIONS[0])
        self.combo=ctk.CTkComboBox(control,values=OPERATIONS,variable=self.op,width=245,height=40,
                                   fg_color=WHITE,border_color="#CAD9D1",button_color=TEAL,
                                   button_hover_color=TEAL_HOVER,text_color=INK,
                                   dropdown_fg_color=WHITE,dropdown_text_color=INK,
                                   font=("Arial",11),command=lambda _v:self.update_status())
        self.combo.grid(row=1,column=0,padx=(20,12),pady=(0,9))
        ctk.CTkLabel(control,text="SCALAR",font=("Arial",9,"bold"),text_color=MUTED).grid(row=1,column=1,padx=(4,7))
        self.scalar=ctk.CTkEntry(control,width=75,height=40,fg_color=WHITE,border_color="#CAD9D1",text_color=INK,justify="center")
        self.scalar.insert(0,"2")
        self.scalar.grid(row=1,column=2,padx=(0,12),pady=(0,9))
        ctk.CTkButton(control,text="Calculate  →",width=130,height=40,corner_radius=10,
                      fg_color=TEAL,hover_color=TEAL_HOVER,text_color=WHITE,
                      font=("Arial",11,"bold"),command=self.calculate).grid(row=1,column=3,padx=5,pady=(0,9))
        ctk.CTkButton(control,text="Reset",width=78,height=40,corner_radius=10,
                      fg_color="#E6EDE7",hover_color="#D8E4DC",text_color=INK,
                      font=("Arial",11,"bold"),command=self.reset).grid(row=1,column=4,padx=(5,18),pady=(0,9))
        self.status=ctk.CTkLabel(control,text="●  A + B REQUIRED",font=("Arial",9,"bold"),text_color=TEAL)
        self.status.grid(row=2,column=0,columnspan=5,sticky="w",padx=22,pady=(0,7))

        # Output section with deep green panel, unlike the previous dark-purple UI.
        result=ctk.CTkFrame(main,fg_color=RESULT,corner_radius=18,border_width=1,border_color="#47716B")
        result.grid(row=4,column=0,columnspan=2,sticky="nsew")
        result.grid_rowconfigure(1,weight=1, minsize=150)
        result.grid_columnconfigure(0,weight=1)
        head=ctk.CTkFrame(result,fg_color="transparent")
        head.grid(row=0,column=0,sticky="ew",padx=20,pady=(9,5))
        ctk.CTkLabel(head,text="Your result",font=("Georgia",18,"bold"),text_color=WHITE).pack(side="left")
        ctk.CTkLabel(head,text="OUTPUT  /  LIVE",font=("Arial",8,"bold"),text_color=CHAMPAGNE).pack(side="right")
        self.output=ctk.CTkTextbox(result,fg_color="#0D3033",text_color="#BCE9D8",
                                   corner_radius=12,border_width=1,border_color="#315C59",
                                   font=("Consolas",13),wrap="none",height=150)
        self.output.grid(row=1,column=0,sticky="nsew",padx=18,pady=(0,12))
        self.show("Your calculated matrix will appear here.\n\nChoose an operation above, then select Calculate.")
        ctk.CTkLabel(main,text="MATRIXLAB LUXE     •     DEEP TEAL / PEARL / CHAMPAGNE",
                     font=("Arial",8,"bold"),text_color="#91B7B2").grid(row=5,column=0,columnspan=2,sticky="w",pady=(7,0))

    def matrix_card(self,parent,name,note,col,defaults):
        card=ctk.CTkFrame(parent,fg_color=PEARL,corner_radius=18,border_width=1,border_color="#D8E2DA")
        card.grid(row=1,column=col,sticky="nsew",padx=(0,8) if col==0 else (8,0))
        ctk.CTkLabel(card,text=f"MATRIX {name}",font=("Georgia",17,"bold"),text_color=INK).pack(anchor="w",padx=18,pady=(9,0))
        ctk.CTkLabel(card,text=note,font=("Arial",8,"bold"),text_color=TEAL).pack(anchor="w",padx=19,pady=(1,5))
        grid=ctk.CTkFrame(card,fg_color="transparent")
        grid.pack(padx=10,pady=(0,9))
        rows=[]
        for r in range(3):
            row=[]
            for c in range(3):
                e=ctk.CTkEntry(grid,width=68,height=34,corner_radius=8,
                               fg_color=WHITE,border_color="#D6E1D9",
                               text_color=INK,placeholder_text_color=MUTED,
                               justify="center",font=("Consolas",13,"bold"))
                e.grid(row=r,column=c,padx=4,pady=3)
                e.insert(0,str(defaults[r][c]))
                row.append(e)
            rows.append(row)
        self.cells[name]=rows

    def read(self,name):
        try: return [[float(self.cells[name][r][c].get()) for c in range(3)] for r in range(3)]
        except ValueError: raise ValueError(f"Matrix {name}: fill every cell with a valid number.")

    def show(self,text):
        self.output.configure(state="normal")
        self.output.delete("1.0","end")
        self.output.insert("1.0",text)
        self.output.configure(state="disabled")

    def update_status(self):
        two=self.op.get() in TWO_MATRIX
        self.status.configure(text="●  A + B REQUIRED" if two else "●  MATRIX A ONLY",
                              text_color=TEAL if two else CORAL)

    def calculate(self):
        try:
            a=self.read("A"); op=self.op.get()
            b=self.read("B") if op in TWO_MATRIX else None
            scalar=float(self.scalar.get()) if op=="Scalar Multiplication (A)" else 1
            result=calculate(op,a,b,scalar)
            self.show(f"OPERATION   /   {op.upper()}\n\n{fmt(result)}")
        except Exception as e:
            self.show("PLEASE CHECK YOUR INPUT\n\n"+str(e))
            messagebox.showerror("MatrixLab",str(e))

    def reset(self):
        defaults={"A":[[1,2,3],[4,5,6],[7,8,9]],"B":[[9,8,7],[6,5,4],[3,2,1]]}
        for name,m in defaults.items():
            for r in range(3):
                for c in range(3):
                    self.cells[name][r][c].delete(0,"end")
                    self.cells[name][r][c].insert(0,str(m[r][c]))
        self.op.set(OPERATIONS[0]); self.scalar.delete(0,"end"); self.scalar.insert(0,"2")
        self.update_status(); self.show("Default sample matrices restored. Ready for a new calculation.")

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1].lower() in ("cmd","cli"): cmd()
    else:
        root=ctk.CTk()
        App(root)
        root.mainloop()
