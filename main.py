from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import json, os
from datetime import datetime

# Arka plan rengi (koyu tema)
Window.clearcolor = (0.1, 0.1, 0.15, 1)
DATA_FILE = "butce_veri.json"

def veri_yukle():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def veri_kaydet(islemler):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(islemler, f, ensure_ascii=False, indent=2)

# Açılır menülerin ekranı kaplamasını engelleyen özel Spinner
class CustomSpinner(Spinner):
    def open_dropdown(self, *args):
        if self._dropdown:
            self._dropdown.max_height = Window.height * 0.5  # Ekranın yarısını geçmesin
        super().open_dropdown(*args)

class ButceApp(App):
    def build(self):
        self.title = "Gelir-Gider Takip"
        self.islemler = veri_yukle()
        
        ana = BoxLayout(orientation="vertical", padding=10, spacing=10)
        
        # --- ÜST BÖLÜM: BAKİYE ---
        self.bakiye_label = Label(text="", font_size="20sp", size_hint=(1, 0.15), markup=True)
        ana.add_widget(self.bakiye_label)
        
        # --- ORTA BÖLÜM: EKLEME FORMU ---
        form = BoxLayout(orientation="vertical", size_hint=(1, 0.45), spacing=8)
        
        # Spinner'ları CustomSpinner ile değiştirdik
        self.tur_spinner = CustomSpinner(text="Gider", values=("Gelir", "Gider"), size_hint=(1, 0.2))
        self.tutar_input = TextInput(hint_text="Tutar (örn: 150.50)", input_filter="float", multiline=False, size_hint=(1, 0.2))
        self.kategori_spinner = CustomSpinner(text="Kategori", values=("Market", "Kira", "Fatura", "Ulaşım", "Maaş", "Ek Gelir", "Diğer"), size_hint=(1, 0.2))
        
        btn_kaydet = Button(text="KAYDET", size_hint=(1, 0.2), background_color=(0.2, 0.7, 0.3, 1), bold=True)
        btn_kaydet.bind(on_press=self.kaydet)
        
        form.add_widget(self.tur_spinner)
        form.add_widget(self.tutar_input)
        form.add_widget(self.kategori_spinner)
        form.add_widget(btn_kaydet)
        ana.add_widget(form)
        
        # --- ALT BÖLÜM: LİSTE ---
        self.scroll = ScrollView(size_hint=(1, 0.4))
        self.liste_kutu = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.liste_kutu.bind(minimum_height=self.liste_kutu.setter("height"))
        self.scroll.add_widget(self.liste_kutu)
        ana.add_widget(self.scroll)
        
        self.liste_yenile()
        self.bakiye_guncelle()
        return ana

    def kaydet(self, instance):
        try:
            tutar = float(self.tutar_input.text.replace(",", "."))
            if tutar <= 0: raise ValueError
        except ValueError:
            self.bakiye_label.text = "[color=ff6666]Hata: Geçerli bir tutar girin![/color]"
            return

        islem = {
            "tur": self.tur_spinner.text,
            "tutar": tutar,
            "kategori": self.kategori_spinner.text,
            "tarih": datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        self.islemler.append(islem)
        veri_kaydet(self.islemler)
        
        self.tutar_input.text = ""
        self.liste_yenile()
        self.bakiye_guncelle()

    def sil(self, index):
        del self.islemler[index]
        veri_kaydet(self.islemler)
        self.liste_yenile()
        self.bakiye_guncelle()

    def liste_yenile(self):
        self.liste_kutu.clear_widgets()
        for i, islem in enumerate(reversed(self.islemler)):
            gercek_idx = len(self.islemler) - 1 - i
            satir = BoxLayout(size_hint_y=None, height=45, spacing=5)
            
            renk = (0.3, 0.9, 0.4, 1) if islem["tur"] == "Gelir" else (1, 0.4, 0.4, 1)
            isaret = "+" if islem["tur"] == "Gelir" else "-"
            
            lbl = Label(text=f"{isaret} {islem['kategori']} ({islem['tarih']})", font_size="13sp", halign="left", valign="middle", color=renk)
            lbl.bind(size=lbl.setter("text_size"))
            
            tutar_lbl = Label(text=f"{islem['tutar']:.2f} TL", font_size="14sp", bold=True, color=renk, size_hint_x=0.4)
            
            btn_sil = Button(text="Sil", size_hint_x=0.2, background_color=(0.6, 0.1, 0.1, 1), font_size="12sp")
            btn_sil.bind(on_press=lambda x, idx=gercek_idx: self.sil(idx))
            
            satir.add_widget(lbl)
            satir.add_widget(tutar_x)
            satir.add_widget(btn_sil)
            self.liste_kutu.add_widget(satir)

    def bakiye_guncelle(self):
        gelir = sum(i["tutar"] for i in self.islemler if i["tur"] == "Gelir")
        gider = sum(i["tutar"] for i in self.islemler if i["tur"] == "Gider")
        bakiye = gelir - gider
        renk = "66ff88" if bakiye >= 0 else "ff6666"
        
        self.bakiye_label.text = (
            f"[color=66ff88]Gelir: {gelir:.2f}[/color]  |  "
            f"[color=ff6666]Gider: {gider:.2f}[/color]\n"
            f"[b][color={renk}]Bakiye: {bakiye:.2f} TL[/color][/b]"
        )

if __name__ == "__main__":
    ButceApp().run()
