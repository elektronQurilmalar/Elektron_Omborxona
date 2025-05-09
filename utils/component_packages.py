# ElektronKomponentlarUchoti/utils/component_packages.py

# Har bir kategoriya uchun korpus turlari ro'yxati
# "Passiv" kategoriya qo'shildi, "Rezistor", "Kondensator", "Induktivlik" o'chirildi
COMPONENT_PACKAGES = {
    "Passiv": [  # YANGI UMUMIY KATEGORIYA
        # Rezistorlar uchun korpuslar
        "01005 (SMD)", "0201 (SMD)", "0402 (SMD)", "0603 (SMD)",
        "0805 (SMD)", "1206 (SMD)", "1210 (SMD)", "1812 (SMD)",
        "2010 (SMD)", "2512 (SMD)",
        "Axial (Through-Hole Rezistor)", "MELF (SMD Rezistor)", "SIP (Rezistorlar to'plami)",
        # Kondensatorlar uchun korpuslar
        # Keramik SMD Kondensator
        # "01005 (SMD)", "0201 (SMD)", ... (yuqorida bor)
        "2220 (SMD Kondensator)",
        # Elektrolitik SMD Kondensator (Aluminium / Polymer)
        "SMD (V-Chip Kondensator)", "SMD (Can Kondensator)",
        # Tantal SMD Kondensator
        "Tantal SMD A (3216)", "Tantal SMD B (3528)", "Tantal SMD C (6032)",
        "Tantal SMD D (7343)", "Tantal SMD E/X (7361)",
        # Through-Hole Kondensator
        "Radial (Elektrolitik/Keramik/Plyonka Kondensator)", "Axial (Elektrolitik/Keramik/Plyonka Kondensator)",
        "Disk (Keramik TH Kondensator)",
        # Induktivliklar uchun korpuslar
        # SMD Induktivlik
        # "0201 (SMD)", ... (yuqorida bor)
        "1008 (SMD Induktivlik)",
        "SMD Power Inductor (Shielded/Unshielded)",
        # Through-Hole Induktivlik
        "Axial (TH Induktivlik)", "Radial (TH Induktivlik)", "Toroidal (TH Induktivlik)",
        "Boshqa (Passiv)"  # Umumiy "Boshqa" passivlar uchun
    ],
    "Diod": [
        "DO-34", "DO-35", "DO-41", "DO-15", "DO-27", "DO-201AD (Axial)",
        "TO-220 (TH Diod)", "TO-247 (TH Diod)",
        "SOD-123", "SOD-323", "SOD-523", "SOD-80 (MELF Diod)", "MiniMELF (Diod)",
        "SOT-23 (Diod)", "SOT-223 (Diod)",
        "SMA (DO-214AC)", "SMB (DO-214AA)", "SMC (DO-214AB)",
        "DFN (Diod)", "QFN (Diod)", "PowerDI",
        "Boshqa (Diod)"
    ],
    "Tranzistor": [
        "TO-18", "TO-39", "TO-92", "TO-126", "TO-220 (Tranzistor)", "TO-247 (Tranzistor)", "TO-3",
        "SOT-23 (Tranzistor)", "SOT-89", "SOT-223 (Tranzistor)", "SOT-323 (Tranzistor)", "SC-70 (SOT-323)", "SC-89",
        "DPAK (TO-252 Tranzistor)", "D2PAK (TO-263 Tranzistor)", "IPAK (TO-251 Tranzistor)",
        "DFN (Tranzistor)", "QFN (Tranzistor)",
        "Boshqa (Tranzistor)"
    ],
    "Mikrokontroller": [
        "DIP-8 (MK)", "DIP-14 (MK)", "DIP-16 (MK)", "DIP-20 (MK)", "DIP-28 (MK)", "DIP-40 (MK)",
        "SOIC-8 (MK)", "SOIC-14 (MK)", "SOIC-16 (MK)", "SOIC-20 (MK)", "SOIC-28 (MK Wide/Narrow)",
        "SSOP (MK)", "TSSOP (MK)", "MSOP (MK)",
        "QFP-32 (MK)", "QFP-44 (MK)", "QFP-64 (MK)", "QFP-80 (MK)", "QFP-100 (MK)", "QFP-144 (MK)",
        "TQFP-32 (MK)", "TQFP-44 (MK)", "TQFP-64 (MK)", "TQFP-100 (MK)", "TQFP-144 (MK)",
        "LQFP-32 (MK)", "LQFP-48 (MK)", "LQFP-64 (MK)", "LQFP-100 (MK)", "LQFP-144 (MK)",
        "PLCC-20 (MK)", "PLCC-28 (MK)", "PLCC-32 (MK)", "PLCC-44 (MK)", "PLCC-52 (MK)", "PLCC-68 (MK)", "PLCC-84 (MK)",
        "QFN (MK)", "DFN (MK)", "MLF (MK)",
        "BGA (MK)", "uBGA (MK)", "WLCSP (MK)",
        "Boshqa (Mikrokontroller)"
    ],
    "DC/DC Mikrosxemalar": [
        "SOT-23-5", "SOT-23-6", "SOT-23-8",
        "TSOT-23-5", "TSOT-23-6",
        "SOT-223 (DC/DC)",
        "SOIC-8 (DC/DC)", "SOIC-14 (DC/DC)", "SOIC-16 (DC/DC Narrow/Wide)",
        "MSOP-8 (DC/DC)", "MSOP-10 (DC/DC)",
        "TSSOP-8 (DC/DC)", "TSSOP-14 (DC/DC)", "TSSOP-16 (DC/DC)", "TSSOP-20 (DC/DC)", "TSSOP-28 (DC/DC)",
        "DFN (DC/DC turli o'lchamlar)", "QFN (DC/DC turli o'lchamlar)",
        "DPAK (TO-252 DC/DC)", "D2PAK (TO-263 DC/DC)",
        "TO-220 (TH DC/DC)", "TO-262 (IPAK-TH DC/DC)",
        "SIP (DC/DC)",
        "Boshqa (DC/DC)"
    ],
    "Mikrosxema (Boshqa)": [
        "DIP-8 (MS)", "DIP-14 (MS)", "DIP-16 (MS)", "DIP-20 (MS)", "DIP-24 (MS)", "DIP-28 (MS)", "DIP-40 (MS)",
        "SOIC-8 (MS)", "SOIC-14 (MS)", "SOIC-16 (MS)", "SOIC-20 (MS)", "SOIC-28 (MS Wide/Narrow)",
        "SSOP (MS)", "TSSOP (MS)", "MSOP (MS)", "SOP (MS)",
        "QFP (MS turli pinlar)", "TQFP (MS)", "LQFP (MS)",
        "PLCC (MS turli pinlar)",
        "BGA (MS)", "uBGA (MS)",
        "QFN (MS)", "DFN (MS)", "SON (MS)",
        "SIP (MS)", "ZIP (MS)",
        "Can (Metall korpus MS, masalan, TO-99)",
        "Boshqa (Mikrosxema)"
    ],
    "Ulagichlar (Konnektorlar)": [
        "JST-XH", "JST-PH", "JST-SM", "JST-ZH",
        "Molex PicoBlade", "Molex Micro-Fit", "Molex Mini-Fit Jr.",
        "Dupont (0.1\" Header/Socket)",
        "IDC Socket/Header",
        "USB-A", "USB-B", "USB-C", "Micro-USB", "Mini-USB",
        "RJ11", "RJ45 (Ethernet)",
        "HDMI", "DisplayPort", "VGA", "DVI",
        "Audio Jack 3.5mm", "Audio Jack 6.35mm", "RCA", "XLR",
        "Barrel Jack (DC Power)", "Terminal Block",
        "DB-9", "DB-15", "DB-25",
        "FFC/FPC Connector", "Card Edge Connector (PCIe, ISA)", "SIM Card Holder",
        "Boshqa (Ulagich)"
    ],
    "Kvars/Osillyator": [
        "HC-49/U (TH Kvars)", "HC-49/S (TH Kvars)", "HC-49/SMD (Kvars)",
        "SMD (7050 Kvars/Os.)", "SMD (5032 Kvars/Os.)", "SMD (3225 Kvars/Os.)", "SMD (2520 Kvars/Os.)",
        "SMD (2016 Kvars/Os.)",
        "Can (Oscillator)", "DIP-8 (Oscillator)", "DIP-14 (Oscillator)",
        "Boshqa (Kvars/Osillyator)"
    ],
    "Rele": [
        "DIP/DIL (Rele)", "SIP (Rele)", "PCB Power Relay", "Automotive Relay", "Solid State Relay (SSR)",
        "Boshqa (Rele)"
    ],
    "Displey/Indikator": [
        "LED (TH 3mm/5mm/etc.)", "LED (SMD 0603/0805/1206/etc.)", "LED 7-Segment",
        "LCD Character Display", "LCD Graphic Display", "OLED Display", "TFT Display",
        "Boshqa (Displey/Indikator)"
    ],
    "Boshqa Komponentlar": [
        "Batareya ushlagich", "Ventilyator", "Radiator", "Knopka (TH/SMD)",
        "Potensiometr", "Enkoder", "Datchik (Sensor)", "Modul (WiFi/BT/GPS)",
        "O'lchamga qarab", "Maxsus korpus", "Noma'lum"
    ]
}


def get_component_types():
    return sorted(list(COMPONENT_PACKAGES.keys()))


def get_packages_for_type(component_type):
    # Agar "Boshqa" bilan tugasa (masalan, "Boshqa (Passiv)"), "Boshqa" ni olib tashlaymiz,
    # chunki COMPONENT_PACKAGES da "Boshqa" bilan tugaydigan qiymatlar bo'lmasligi kerak.
    # "Boshqa" har doim ro'yxat oxirida qo'shiladi.
    clean_type = component_type.replace(" (Passiv)", "").replace(" (Diod)", "").replace(" (Tranzistor)",
                                                                                        "")  # va hokazo

    default_packages_list = ["Boshqa"]  # Standart qiymat, agar kategoriya topilmasa

    # COMPONENT_PACKAGES.get(component_type, ...) component_type uchun aniq moslikni qidiradi
    # Agar bizda "Passiv" kategoriyasi bo'lsa va component_type "Passiv" bo'lsa, u to'g'ri ishlaydi.
    packages = COMPONENT_PACKAGES.get(component_type, default_packages_list)

    # "Boshqa" elementi har doim mavjud bo'lishini ta'minlash
    # Agar component_type uchun maxsus "Boshqa (KategoriyaNomi)" mavjud bo'lsa, umumiy "Boshqa" ni qo'shmaymiz.
    # Aks holda, umumiy "Boshqa" ni qo'shamiz.

    # Barcha paketlarni yig'ish va takrorlanmas qilish
    unique_packages = set(packages)

    # Har bir kategoriya uchun o'zining "Boshqa (Kategoriya)" bo'lishi mumkin,
    # yoki umumiy "Boshqa"
    # Misol: "Boshqa (Passiv)" "Passiv" kategoriyasi uchun
    # Umumiy "Boshqa" ni qo'shamiz, agar maxsus "Boshqa (...)" bo'lmasa

    specific_boshqa = f"Boshqa ({component_type})"  # Misol: "Boshqa (Diod)"
    if specific_boshqa not in unique_packages and "Boshqa" not in unique_packages:
        unique_packages.add("Boshqa")

    # Agar packages aslida default_packages_list bo'lsa (ya'ni, component_type topilmagan bo'lsa),
    # unda faqat ["Boshqa"] qoladi. Bu to'g'ri.

    return sorted(list(unique_packages))