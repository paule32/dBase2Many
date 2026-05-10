from pathlib import Path
import subprocess


INKSCAPE_EXE = Path(r"T:\Program Files\Inkscape\bin\inkscape.exe")

FLAG_COUNTRY_MAP = {
    "ENU": "us",
    "ENG": "gb",
    "DEU": "de",
    "FRA": "fr",
    "ESP": "es",
    "ITA": "it",
    "NLD": "nl",
    "PTB": "br",
    "POR": "pt",
    "PLK": "pl",
    "RUS": "ru",

    "AFR": "za",
    "ALB": "al",
    "ARA": "sa",
    "ARM": "am",
    "AZE": "az",
    "BAQ": "es",
    "BEL": "by",
    "BEN": "bd",
    "BOS": "ba",
    "BGR": "bg",
    "CAT": "es",
    "CHS": "cn",
    "CHT": "tw",
    "HRV": "hr",
    "CSY": "cz",
    "DAN": "dk",
    "ETI": "ee",
    "FIN": "fi",
    "GLC": "es",
    "GEO": "ge",
    "ELL": "gr",
    "HEB": "il",
    "HIN": "in",
    "HUN": "hu",
    "ISL": "is",
    "IND": "id",
    "GLE": "ie",
    "JPN": "jp",
    "KAN": "in",
    "KAZ": "kz",
    "KOR": "kr",
    "LVI": "lv",
    "LTH": "lt",
    "MKD": "mk",
    "MSL": "my",
    "MAL": "in",
    "MAR": "in",
    "MON": "mn",
    "NEP": "np",
    "NOR": "no",
    "NOB": "no",
    "NNO": "no",
    "FAR": "ir",
    "ROM": "ro",
    "SRB": "rs",
    "SRL": "rs",
    "SKY": "sk",
    "SLV": "si",
    "SVE": "se",
    "SWA": "tz",
    "TAM": "in",
    "TEL": "in",
    "THA": "th",
    "TRK": "tr",
    "UKR": "ua",
    "URD": "pk",
    "VIT": "vn",
}


def convert_svg_to_png(svg_path: Path, png_path: Path, width: int = 22, height: int = 12):
    png_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        str(INKSCAPE_EXE),
        str(svg_path),
        "--export-type=png",
        f"--export-filename={png_path}",
        f"--export-width={width}",
        f"--export-height={height}",
    ]

    subprocess.run(cmd, check=True)


def write_qrc(output_flags_dir: Path, qrc_path: Path):
    lines = [
        "<RCC>",
        '    <qresource prefix="/flags">',
    ]

    for code in sorted(FLAG_COUNTRY_MAP.keys()):
        filename = f"{code.lower()}.png"
        lines.append(f'        <file alias="{filename}">flags/{filename}</file>')

    lines.extend([
        "    </qresource>",
        "</RCC>",
        "",
    ])

    qrc_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    if not INKSCAPE_EXE.exists():
        raise FileNotFoundError(f"Inkscape nicht gefunden: {INKSCAPE_EXE}")

    # Pfad zum entpackten flag-icons Paket:
    flag_icons_dir = Path(r"../images/flags")

    # In flag-icons:
    source_dir = flag_icons_dir / "4x3"

    # Ziel in deinem dBase2Many-Projekt:
    project_res_dir = Path(r"../share/resrces")

    output_flags_dir = project_res_dir / "flags"
    qrc_path = project_res_dir / "flags.qrc"

    missing = []

    for lang_code, country_code in FLAG_COUNTRY_MAP.items():
        svg_path = source_dir / f"{country_code.lower()}.svg"
        png_path = output_flags_dir / f"{lang_code.lower()}.png"

        if not svg_path.exists():
            missing.append((lang_code, country_code, svg_path))
            continue

        convert_svg_to_png(svg_path, png_path, 22, 12)
        print(f"{lang_code} -> {country_code}: {png_path}")

    write_qrc(output_flags_dir, qrc_path)

    if missing:
        print()
        print("Fehlende SVG-Dateien:")
        for lang_code, country_code, svg_path in missing:
            print(f"{lang_code} -> {country_code}: {svg_path}")

    print()
    print("Fertig.")
    print(f"PNG-Flaggen: {output_flags_dir}")
    print(f"QRC-Datei:   {qrc_path}")


if __name__ == "__main__":
    main()
