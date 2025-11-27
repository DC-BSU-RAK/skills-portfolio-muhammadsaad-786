import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

# Choosing the App Theme
BG_MAIN = "#1e1e2e"
BG_SIDE = "#282a36"
FG_TEXT = "#f8f8f2"
ACCENT = "#bd93f9"
BTN_BG = "#44475a"
BTN_HOVER = "#6272a4"

class StudentManager:
    def __init__(self, window):
        self.win = window
        self.win.title("Student Manager - Ultimate Fascinating Edition")
        self.win.geometry("1400x900")
        self.win.configure(bg=BG_MAIN)

        # state variables
        self.records = []
        self.db_file = self.locate_db()
        self.curr_sort_col = "percent"
        self.sort_desc = True

        # Initial load
        self.load_records()
        self.init_interface()
        self.populate_table()

    def locate_db(self):
        filename = "studentMarks.txt"
        current_dir = os.path.dirname(__file__)
        
        candidates = [
            filename,
            os.path.join(current_dir, filename),
            f"resources/{filename}",
            os.path.join(current_dir, "resources", filename)
        ]

        for path in candidates:
            if os.path.exists(path):
                return os.path.abspath(path)
        
        return filename

    def calculate_grade(self, percentage):
        if percentage >= 70: return "A"
        if percentage >= 60: return "B"
        if percentage >= 50: return "C"
        if percentage >= 40: return "D"
        return "F"

    def load_records(self):
        self.records = []
        
        # Ensuring that file exists
        if not os.path.exists(self.db_file):
            with open(self.db_file, "w") as f:
                f.write("0\n")
            return

        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                content = f.readlines()

            # Processing lines and skipping empty ones
            valid_lines = [x.strip() for x in content if x.strip()]
            if not valid_lines: 
                return

            # Skipping the first line and processing the rest
            for line in valid_lines[1:]:
                parts = line.split(",")
                if len(parts) < 6: 
                    continue

                # Parse data
                code = parts[0].strip()
                name = parts[1].strip()
                c1 = int(parts[2])
                c2 = int(parts[3])
                c3 = int(parts[4])
                exam = int(parts[5])

                total_cw = c1 + c2 + c3
                grand_total = total_cw + exam
                pct = round((grand_total / 160) * 100, 2)
                grade = self.calculate_grade(pct)

                self.records.append({
                    "code": code,
                    "name": name,
                    "cw1": c1, "cw2": c2, "cw3": c3,
                    "coursework": total_cw,
                    "exam": exam,
                    "total": grand_total,
                    "percent": pct,
                    "grade": grade
                })

        except ValueError:
            messagebox.showerror("Data Error", "Corrupt data found in file. Check number formats.")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to read file:\n{e}")

    def save_records(self):
        try:
            with open(self.db_file, "w", encoding="utf-8") as f:
                f.write(f"{len(self.records)}\n")
                for r in self.records:
                    line = f"{r['code']},{r['name']},{r['cw1']},{r['cw2']},{r['cw3']},{r['exam']}\n"
                    f.write(line)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save changes:\n{e}")

    def init_interface(self):
        # Sidebar layout
        pnl_side = tk.Frame(self.win, bg=BG_SIDE, width=250, relief="raised", bd=2)
        pnl_side.pack(side="left", fill="y", padx=10, pady=10)

        lbl_title = tk.Label(pnl_side, text="Student Nexus", font=("Arial", 24, "bold"), bg=BG_SIDE, fg=ACCENT)
        lbl_title.pack(pady=30)

        # Sidebar Menu Actions
        menu_items = [
            ("View All Records", self.action_view_all),
            ("View Individual", self.action_find_one),
            ("Highest Score", self.action_highest),
            ("Lowest Score", self.action_lowest),
            ("Sort Records", self.action_sort_ui),
            ("Add Student", self.ui_add_student),
            ("Delete Student", self.action_delete),
            ("Update Student", self.ui_update_student),
        ]

        for txt, func in menu_items:
            btn = tk.Button(pnl_side, text=txt, font=("Arial", 13, "bold"), 
                            bg=BTN_BG, fg=FG_TEXT, activebackground=ACCENT, 
                            activeforeground=BG_SIDE, relief="groove", bd=3, 
                            padx=15, pady=8, command=func)
            btn.pack(fill="x", pady=8, padx=15)
            
            # Adding Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=BTN_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=BTN_BG))

        # Making the Main Area
        pnl_main = tk.Frame(self.win, bg=BG_MAIN)
        pnl_main.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Developing the Stats Header
        self.lbl_stats = tk.Label(pnl_main, text="Total Students: 0 | Average %: 0.00", 
                                  font=("Arial", 16), bg=BG_MAIN, fg="#8be9fd")
        self.lbl_stats.pack(pady=10)

        # Adding a Search Bar
        pnl_search = tk.Frame(pnl_main, bg=BG_MAIN)
        pnl_search.pack(fill="x", pady=10)
        
        tk.Label(pnl_search, text="Search:", bg=BG_MAIN, fg="#f1fa8c", font=("Arial", 14)).pack(side="left", padx=20)
        
        self.search_val = tk.StringVar()
        self.search_val.trace("w", lambda *args: self.populate_table()) # Adding Auto search on type
        
        ent_search = tk.Entry(pnl_search, textvariable=self.search_val, font=("Arial", 14), 
                              bg=BTN_BG, fg="white", insertbackground="white", width=50)
        ent_search.pack(side="left", padx=20)

        # Adding Treeview or Table
        self.setup_treeview(pnl_main)

    def setup_treeview(self, parent):
        # Style config
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG_SIDE, foreground=FG_TEXT, fieldbackground=BG_SIDE, rowheight=40, font=("Arial", 12))
        style.configure("Treeview.Heading", background=BTN_BG, foreground=ACCENT, font=("Arial", 13, "bold"))
        style.map("Treeview", background=[("selected", BTN_HOVER)])

        cols = ("code", "name", "cw", "exam", "pct", "grade")
        self.tree = ttk.Treeview(parent, columns=cols, show="headings")

        # Making Column definitions
        headers = [
            ("code", "Code", 120),
            ("name", "Name", 350),
            ("cw", "Coursework /60", 150),
            ("exam", "Exam /100", 150),
            ("pct", "Percent %", 130),
            ("grade", "Grade", 110)
        ]

        for col_id, title, w in headers:
            mapping = {"cw": "coursework", "pct": "percent"} # Map display ID to internal key
            sort_key = mapping.get(col_id, col_id)
            
            self.tree.heading(col_id, text=title, command=lambda c=sort_key: self.sort_data(c))
            self.tree.column(col_id, width=w, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=10)

        # Adding a Scrollbar
        sb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=sb.set)

        # Adding Row Tags for Grade Colors
        color_map = {
            "A": "#50fa7b", "B": "#8be9fd", "C": "#f1fa8c", 
            "D": "#ffb86c", "F": "#ff5555"
        }
        for g, col in color_map.items():
            self.tree.tag_configure(g, background=col, foreground=BG_SIDE)

    def update_stats_display(self):
        total = len(self.records)
        avg_score = 0
        if total > 0:
            avg_score = sum(r["percent"] for r in self.records) / total
        self.lbl_stats.config(text=f"Total Students: {total} | Average %: {avg_score:.2f}")

    def populate_table(self):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        search_term = self.search_val.get().lower()
        
        # Sorting logic
        display_data = sorted(self.records, key=lambda x: x.get(self.curr_sort_col, 0), reverse=self.sort_desc)

        for r in display_data:
            # Adding Filter
            if search_term in r["name"].lower() or search_term in r["code"]:
                vals = (
                    r["code"], 
                    r["name"], 
                    r["coursework"], 
                    r["exam"], 
                    f"{r['percent']:.2f}", 
                    r["grade"]
                )
                self.tree.insert("", "end", values=vals, tags=(r["grade"],))
        
        self.update_stats_display()

    def sort_data(self, col_key):
        # Toggle the direction if clicking same column
        if self.curr_sort_col == col_key:
            self.sort_desc = not self.sort_desc
        else:
            self.curr_sort_col = col_key
            self.sort_desc = True # Default to desc for new col
            
        self.populate_table()

    # Customizing the Actions

    def action_view_all(self):
        self.populate_table()
        count = len(self.records)
        avg = sum(r["percent"] for r in self.records) / count if count else 0
        messagebox.showinfo("Class Summary", f"Students: {count}\nAverage: {avg:.2f}%")

    def action_find_one(self):
        q = simpledialog.askstring("Search Student", "Enter name or code:")
        if not q: return

        found = None
        for r in self.records:
            if q == r["code"] or q.lower() in r["name"].lower():
                found = r
                break
        
        if found:
            details = (f"Name: {found['name']}\nCode: {found['code']}\n"
                       f"Coursework: {found['coursework']}/60\n"
                       f"Exam: {found['exam']}/100\n"
                       f"Percent: {found['percent']:.2f}%\n"
                       f"Grade: {found['grade']}")
            messagebox.showinfo("Student Details", details)
        else:
            messagebox.showwarning("Not Found", "Student not found.")

    def action_highest(self):
        if not self.records: return
        top = max(self.records, key=lambda x: x["percent"])
        info = (f"Name: {top['name']}\nCode: {top['code']}\n"
                f"Coursework: {top['coursework']}/60\nExam: {top['exam']}/100\n"
                f"Percent: {top['percent']:.2f}%\nGrade: {top['grade']}")
        messagebox.showinfo("Highest Score", info)

    def action_lowest(self):
        if not self.records: return
        low = min(self.records, key=lambda x: x["percent"])
        info = (f"Name: {low['name']}\nCode: {low['code']}\n"
                f"Coursework: {low['coursework']}/60\nExam: {low['exam']}/100\n"
                f"Percent: {low['percent']:.2f}%\nGrade: {low['grade']}")
        messagebox.showinfo("Lowest Score", info)

    def action_sort_ui(self):
        self.sort_data("percent")
        messagebox.showinfo("Sorted", "Records sorted by percentage (descending). Click headers for more.")

    def action_delete(self):
        cur = self.tree.selection()
        if not cur:
            messagebox.showwarning("Select", "Select a student from the table first.")
            return

        row_vals = self.tree.item(cur[0])["values"]
        s_code = str(row_vals[0]) # ensure string for comparison
        s_name = row_vals[1]

        confirm = messagebox.askyesno("Confirm Delete", f"Delete student {s_code} - {s_name}?")
        if confirm:
            # Filter out the deleted student
            self.records = [x for x in self.records if str(x["code"]) != s_code]
            self.save_records()
            self.populate_table()
            messagebox.showinfo("Deleted", "Student removed successfully!")

    # Adding or Updating Modals

    def create_input_modal(self, title, btn_text, cmd_callback, defaults=None):
        pop = tk.Toplevel(self.win)
        pop.title(title)
        pop.geometry("400x500")
        pop.configure(bg=BG_MAIN)

        labels = ["Student Code (1000-9999)" if not defaults else "Full Name", 
                  "Full Name" if not defaults else "CW1 (/20)", 
                  "CW1 (/20)" if not defaults else "CW2 (/20)", 
                  "CW2 (/20)" if not defaults else "CW3 (/20)", 
                  "CW3 (/20)" if not defaults else "Exam (/100)", 
                  "Exam (/100)" if not defaults else None]

        entries = []
        
        # Adjust input list based on whether we are adding or updating
        iter_labels = [l for l in labels if l is not None]

        for i, txt in enumerate(iter_labels):
            tk.Label(pop, text=txt, bg=BG_MAIN, fg="#f1fa8c", font=("Arial", 12)).pack(pady=5)
            ent = tk.Entry(pop, bg=BTN_BG, fg="white", insertbackground="white", font=("Arial", 12))
            
            if defaults and i < len(defaults):
                ent.insert(0, str(defaults[i]))
            
            ent.pack(pady=5)
            entries.append(ent)

        action_btn = tk.Button(pop, text=btn_text, command=lambda: cmd_callback(entries, pop), 
                               bg=BTN_HOVER, fg="white", font=("Arial", 12, "bold"))
        action_btn.pack(pady=20)

    def ui_add_student(self):
        self.create_input_modal("Add New Student", "Add", self.process_add)

    def process_add(self, fields, window):
        try:
            # Extracting
            code = fields[0].get().strip()
            name = fields[1].get().strip()
            cw1 = int(fields[2].get())
            cw2 = int(fields[3].get())
            cw3 = int(fields[4].get())
            exam = int(fields[5].get())

            # Calculating
            cw_total = cw1 + cw2 + cw3
            final = cw_total + exam
            pct = round((final / 160) * 100, 2)
            grd = self.calculate_grade(pct)

            # For Storing
            self.records.append({
                "code": code, "name": name, 
                "cw1": cw1, "cw2": cw2, "cw3": cw3,
                "coursework": cw_total, "exam": exam, 
                "total": final, "percent": pct, "grade": grd
            })
            
            self.save_records()
            self.populate_table()
            window.destroy()
            messagebox.showinfo("Success", "Student added!")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure marks are numbers.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ui_update_student(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a student from the table first.")
            return

        # For Finding data
        code_val = str(self.tree.item(sel[0])["values"][0])
        student = next((x for x in self.records if str(x["code"]) == code_val), None)
        
        if not student: return

        # Prefill data
        current_data = [student["name"], student["cw1"], student["cw2"], student["cw3"], student["exam"]]
        
        # Pass the student object to the callback using a helper wrapper
        def callback_wrapper(entries, win):
            self.process_update(student, entries, win)

        self.create_input_modal("Update Student", "Update", callback_wrapper, defaults=current_data)

    def process_update(self, student_dict, fields, window):
        try:
            name = fields[0].get().strip()
            cw1 = int(fields[1].get())
            cw2 = int(fields[2].get())
            cw3 = int(fields[3].get())
            exam = int(fields[4].get())

            cw_total = cw1 + cw2 + cw3
            final = cw_total + exam
            pct = round((final / 160) * 100, 2)
            grd = self.calculate_grade(pct)

            # Update dictionary in place
            student_dict.update({
                "name": name,
                "cw1": cw1, "cw2": cw2, "cw3": cw3,
                "coursework": cw_total,
                "exam": exam,
                "total": final,
                "percent": pct,
                "grade": grd
            })

            self.save_records()
            self.populate_table()
            window.destroy()
            messagebox.showinfo("Success", "Student updated successfully!")

        except ValueError:
            messagebox.showerror("Input Error", "Please ensure marks are numbers.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()