import tkinter as tk
from tkinter import ttk, messagebox


class FitnessKalkulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Napredni Fitness Kalkulator")
        self.root.geometry("750x850")
        self.root.configure(bg="#f0f2f5")

        # Stilizacija
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#f0f2f5")
        self.style.configure('TLabel', background="#f0f2f5", font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=6)
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Result.TLabel', font=('Helvetica', 10, 'bold'))
        self.style.configure('Table.TLabel', font=('Helvetica', 9), padding=5)
        self.style.configure('TableHeader.TLabel', font=('Helvetica', 9, 'bold'), padding=5)

        # Boje
        self.primary_color = "#4e73df"
        self.secondary_color = "#1cc88a"
        self.accent_color = "#f6c23e"
        self.dark_color = "#5a5c69"

        self.kreiraj_widgete()

    def kreiraj_widgete(self):
        # Zaglavlje
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ttk.Label(
            header_frame,
            text="NAPREDNI FITNESS KALKULATOR",
            style='Header.TLabel',
            foreground=self.primary_color
        ).pack()

        ttk.Label(
            header_frame,
            text="Izračunajte svoj BMI, TDEE i makronutrijente",
            style='TLabel',
            foreground=self.dark_color
        ).pack()

        # Sekcija za unos
        input_frame = ttk.LabelFrame(self.root, text=" Vaši podaci ", padding=15)
        input_frame.pack(fill="x", padx=20, pady=10)

        # Redovi za unos
        input_rows = [
            ("Težina (kg):", "weight_entry", "Unesite svoju težinu u kilogramima"),
            ("Visina (cm):", "height_entry", "Unesite svoju visinu u centimetrima"),
            ("Godine:", "age_entry", "Unesite svoje godine")
        ]

        for i, (label_text, var_name, tooltip) in enumerate(input_rows):
            row_frame = ttk.Frame(input_frame)
            row_frame.pack(fill="x", pady=5)

            label = ttk.Label(row_frame, text=label_text, width=15, anchor="e")
            label.pack(side="left", padx=(0, 10))

            entry = ttk.Entry(row_frame)
            entry.pack(side="left", expand=True, fill="x")

            setattr(self, var_name, entry)

            # Dodaj tooltip
            self.kreiraj_tooltip(entry, tooltip)

        # Pol
        gender_frame = ttk.Frame(input_frame)
        gender_frame.pack(fill="x", pady=5)

        ttk.Label(
            gender_frame,
            text="Pol:",
            width=15,
            anchor="e"
        ).pack(side="left", padx=(0, 10))

        self.gender_var = tk.StringVar(value="Muški")

        male_btn = ttk.Radiobutton(
            gender_frame,
            text="Muški",
            variable=self.gender_var,
            value="Muški"
        )
        male_btn.pack(side="left", padx=(0, 10))

        female_btn = ttk.Radiobutton(
            gender_frame,
            text="Ženski",
            variable=self.gender_var,
            value="Ženski"
        )
        female_btn.pack(side="left")

        # Nivo aktivnosti
        activity_frame = ttk.Frame(input_frame)
        activity_frame.pack(fill="x", pady=5)

        ttk.Label(
            activity_frame,
            text="Nivo aktivnosti:",
            width=15,
            anchor="e"
        ).pack(side="left", padx=(0, 10))

        self.activity_var = tk.StringVar()

        activity_choices = [
            "Sedentaran (malo ili nimalo vežbanja)",
            "Lagano aktivan (lagano vežbanje 1-3 dana/nedelju)",
            "Umereno aktivan (umereno vežbanje 3-5 dana/nedelju)",
            "Veoma aktivan (intenzivno vežbanje 6-7 dana/nedelju)",
            "Ekstremno aktivan (vrlo teško vežbanje i fizički posao)"
        ]

        self.activity_combobox = ttk.Combobox(
            activity_frame,
            textvariable=self.activity_var,
            values=activity_choices,
            state="readonly"
        )

        self.activity_combobox.current(0)
        self.activity_combobox.pack(side="left", expand=True, fill="x")

        # Ishrana
        diet_frame = ttk.Frame(input_frame)
        diet_frame.pack(fill="x", pady=5)

        ttk.Label(
            diet_frame,
            text="Tip ishrane:",
            width=15,
            anchor="e"
        ).pack(side="left", padx=(0, 10))

        self.diet_var = tk.StringVar()

        diet_choices = [
            "Standardna (40% ugljeni hidrati, 30% proteini, 30% masti)",
            "Nizak unos ugljenih hidrata (30% ugljeni hidrati, 35% proteini, 35% masti)"
        ]

        self.diet_combobox = ttk.Combobox(
            diet_frame,
            textvariable=self.diet_var,
            values=diet_choices,
            state="readonly"
        )

        self.diet_combobox.current(0)
        self.diet_combobox.pack(side="left", expand=True, fill="x")

        # Dugme za izračunavanje
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=(10, 20))

        self.calculate_btn = ttk.Button(
            btn_frame,
            text="IZRAČUNAJ REZULTATE",
            command=self.izracunaj_rezultate,
            style='TButton'
        )
        self.calculate_btn.pack(pady=5, ipadx=20, ipady=5)

        # Sekcija za rezultate
        self.results_frame = ttk.LabelFrame(self.root, text=" Vaši rezultati ", padding=15)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Početni tekst
        ttk.Label(
            self.results_frame,
            text="Unesite svoje podatke i kliknite 'Izračunaj rezultate'",
            style='TLabel',
            foreground=self.dark_color
        ).pack(expand=True)

    def kreiraj_tooltip(self, widget, text):
        tooltip = tk.Toplevel(self.root)
        tooltip.withdraw()
        tooltip.overrideredirect(True)

        label = ttk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1
        )
        label.pack()

        def enter(event):
            bbox = widget.bbox("insert")

            if bbox is None:
                x = widget.winfo_rootx() + 25
                y = widget.winfo_rooty() + 25
            else:
                x, y, _, _ = bbox
                x += widget.winfo_rootx() + 25
                y += widget.winfo_rooty() + 25

            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def leave(event):
            tooltip.withdraw()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def izracunaj_rezultate(self):
        try:
            # Unos podataka
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # pretvori u metre
            age = int(self.age_entry.get())
            gender = self.gender_var.get()

            activity_level = self.activity_var.get().split(" ")[0]

            diet_type = (
                "Nizak unos ugljenih hidrata"
                if "Nizak" in self.diet_var.get()
                else "Standardna"
            )

            if weight <= 0 or height <= 0 or age <= 0:
                messagebox.showerror(
                    "Greška",
                    "Unesite validne pozitivne vrednosti"
                )
                return

            # BMI izračun
            bmi = weight / (height ** 2)
            bmi = round(bmi, 1)

            # BMI kategorija
            if bmi < 18.5:
                category = "Pothranjenost"
                category_color = "#36b9cc"
            elif 18.5 <= bmi < 25:
                category = "Normalna težina"
                category_color = "#1cc88a"
            elif 25 <= bmi < 30:
                category = "Prekomerna težina"
                category_color = "#f6c23e"
            else:
                category = "Gojaznost"
                category_color = "#e74a3b"

            # Normalan opseg težine
            min_normal = 18.5 * (height ** 2)
            max_normal = 24.9 * (height ** 2)
            normal_range = f"{round(min_normal, 1)} - {round(max_normal, 1)} kg"

            # Bazalni metabolizam (BMR)
            if gender == "Muški":
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * (height * 100) - 5 * age - 161

            # Multiplikatori aktivnosti
            activity_multipliers = {
                "Sedentaran": 1.2,
                "Lagano": 1.375,
                "Umereno": 1.55,
                "Veoma": 1.725,
                "Ekstremno": 1.9
            }

            # TDEE izračun
            tdee = round(bmr * activity_multipliers[activity_level])

            # Makronutrijenti
            def izracunaj_makroe(calories, low_carb=False):
                if low_carb:
                    # Nizak unos ugljenih hidrata
                    # 30% ugljeni hidrati, 35% proteini, 35% masti
                    carbs = round((calories * 0.3) / 4)
                    protein = round((calories * 0.35) / 4)
                    fat = round((calories * 0.35) / 9)
                else:
                    # Standardni odnos
                    # 40% ugljeni hidrati, 30% proteini, 30% masti
                    carbs = round((calories * 0.4) / 4)
                    protein = round((calories * 0.3) / 4)
                    fat = round((calories * 0.3) / 9)

                return carbs, protein, fat

            # Svi scenariji
            maintenance_cals = tdee
            cutting_cals = tdee - 500
            bulking_cals = tdee + 500

            # Makroi
            m_carbs, m_protein, m_fat = izracunaj_makroe(
                maintenance_cals,
                diet_type == "Nizak unos ugljenih hidrata"
            )

            c_carbs, c_protein, c_fat = izracunaj_makroe(
                cutting_cals,
                diet_type == "Nizak unos ugljenih hidrata"
            )

            b_carbs, b_protein, b_fat = izracunaj_makroe(
                bulking_cals,
                diet_type == "Nizak unos ugljenih hidrata"
            )

            # Obriši prethodne rezultate
            for widget in self.results_frame.winfo_children():
                widget.destroy()

            # Kreiraj kontejner sa scrollbar-om
            canvas = tk.Canvas(
                self.results_frame,
                bg="#f0f2f5",
                highlightthickness=0
            )

            scrollbar = ttk.Scrollbar(
                self.results_frame,
                orient="vertical",
                command=canvas.yview
            )

            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            # Osnovne informacije
            info_frame = ttk.Frame(scrollable_frame)
            info_frame.pack(fill="x", padx=5, pady=10)

            ttk.Label(
                info_frame,
                text="OSNOVNE INFORMACIJE",
                style='Header.TLabel',
                foreground=self.primary_color
            ).pack(anchor="w", pady=(0, 10))

            # BMI red
            bmi_row = ttk.Frame(info_frame)
            bmi_row.pack(fill="x", pady=2)

            ttk.Label(
                bmi_row,
                text="BMI:",
                width=20,
                anchor="w"
            ).pack(side="left")

            ttk.Label(
                bmi_row,
                text=f"{bmi} ({category})",
                style='Result.TLabel',
                foreground=category_color
            ).pack(side="left")

            # Normalan opseg težine
            weight_row = ttk.Frame(info_frame)
            weight_row.pack(fill="x", pady=2)

            ttk.Label(
                weight_row,
                text="Normalan opseg težine:",
                width=20,
                anchor="w"
            ).pack(side="left")

            ttk.Label(
                weight_row,
                text=normal_range,
                style='Result.TLabel',
                foreground=self.dark_color
            ).pack(side="left")

            # TDEE
            tdee_row = ttk.Frame(info_frame)
            tdee_row.pack(fill="x", pady=2)

            ttk.Label(
                tdee_row,
                text="Dnevne kalorijske potrebe (TDEE):",
                width=20,
                anchor="w"
            ).pack(side="left")

            ttk.Label(
                tdee_row,
                text=f"{tdee} kcal/dan",
                style='Result.TLabel',
                foreground=self.primary_color
            ).pack(side="left")

            # Nivo aktivnosti
            activity_row = ttk.Frame(info_frame)
            activity_row.pack(fill="x", pady=2)

            ttk.Label(
                activity_row,
                text="Nivo aktivnosti:",
                width=20,
                anchor="w"
            ).pack(side="left")

            ttk.Label(
                activity_row,
                text=self.activity_var.get(),
                style='Result.TLabel',
                foreground=self.dark_color
            ).pack(side="left")

            # Tip ishrane
            diet_row = ttk.Frame(info_frame)
            diet_row.pack(fill="x", pady=2)

            ttk.Label(
                diet_row,
                text="Tip ishrane:",
                width=20,
                anchor="w"
            ).pack(side="left")

            ttk.Label(
                diet_row,
                text=diet_type,
                style='Result.TLabel',
                foreground=self.dark_color
            ).pack(side="left")

            # Makronutrijenti
            macro_frame = ttk.Frame(scrollable_frame)
            macro_frame.pack(fill="x", padx=5, pady=(20, 10))

            ttk.Label(
                macro_frame,
                text="MAKRONUTRIJENTNI PLANOVI",
                style='Header.TLabel',
                foreground=self.primary_color
            ).pack(anchor="w", pady=(0, 10))

            # Tabela
            table_frame = ttk.Frame(macro_frame)
            table_frame.pack(fill="x")

            # Zaglavlja tabele
            headers = [
                "Plan",
                "Kalorije",
                "Ugljeni hidrati (g)",
                "Proteini (g)",
                "Masti (g)"
            ]

            for col, header in enumerate(headers):
                ttk.Label(
                    table_frame,
                    text=header,
                    style='TableHeader.TLabel',
                    foreground="#ffffff",
                    background=self.primary_color,
                    anchor="center"
                ).grid(row=0, column=col, sticky="nsew", padx=1, pady=1)

            # Podaci tabele
            data = [
                ["Održavanje", maintenance_cals, m_carbs, m_protein, m_fat],
                ["Mršavljenje (-500 kcal)", cutting_cals, c_carbs, c_protein, c_fat],
                ["Dobijanje mase (+500 kcal)", bulking_cals, b_carbs, b_protein, b_fat]
            ]

            colors = [
                self.secondary_color,
                self.accent_color,
                "#e74a3b"
            ]

            for row, (row_data, color) in enumerate(zip(data, colors), start=1):
                for col, value in enumerate(row_data):
                    bg_color = "#ffffff" if col != 0 else color
                    fg_color = "#000000" if col != 0 else "#ffffff"
                    anchor = "w" if col == 0 else "center"

                    ttk.Label(
                        table_frame,
                        text=value,
                        style='Table.TLabel',
                        background=bg_color,
                        foreground=fg_color,
                        anchor=anchor
                    ).grid(row=row, column=col, sticky="nsew", padx=1, pady=1)

            # Podešavanje težina kolona
            for col in range(len(headers)):
                table_frame.grid_columnconfigure(col, weight=1)

            # Napomene
            notes_frame = ttk.Frame(scrollable_frame)
            notes_frame.pack(fill="x", padx=5, pady=(20, 10))

            ttk.Label(
                notes_frame,
                text="NAPOMENE",
                style='Header.TLabel',
                foreground=self.primary_color
            ).pack(anchor="w", pady=(0, 5))

            notes = [
                "• TDEE (ukupna dnevna potrošnja energije) predstavlja kalorije za održavanje",
                "• Mršavljenje: 500 kcal manje za postepeno gubljenje masti (oko 0.5 kg nedeljno)",
                "• Dobijanje mase: 500 kcal više za postepeno dobijanje mišića",
                f"• Odnos makronutrijenta baziran na planu ishrane: {diet_type.lower()}"
            ]

            for note in notes:
                ttk.Label(
                    notes_frame,
                    text=note,
                    style='TLabel',
                    foreground=self.dark_color
                ).pack(anchor="w", pady=2)

            # Ažuriraj scroll region
            canvas.configure(scrollregion=canvas.bbox("all"))

        except ValueError:
            messagebox.showerror(
                "Greška",
                "Unesite validne brojeve u sva polja"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessKalkulator(root)
    root.mainloop()