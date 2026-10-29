import psycopg2


def bazaga_ulan():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="test",
            user="postgres",
            password="",  # ⚠️ O'Z PAROLINGIZNI YOZING
            port="5432",
        )
        return connection, connection.cursor()
    except Exception as error:
        print("Baza bilan ulanishda xatolik:", error)
        return None, None


# BAZADAN MA'LUMOT OLIB CHIQUVCHI ASOSIY FUNKSIYA
def bazadan_ism_boyicha_ol(qidirilayotgan_ism):
    conn, cursor = bazaga_ulan()
    if not conn:
        return

    try:
        # SQL so'rovi: Python bazadan ma'lumotni so'rayapti
        sql_query = "SELECT id, ism, familiya, lavozim, maosh FROM xodimlar WHERE ism ILIKE %s;"

        # Biz yozgan ismni xavfsiz formatga o'tkazamiz (masalan: %sardor%)
        formatlangan_ism = f"%{qidirilayotgan_ism}%"

        cursor.execute(sql_query, (formatlangan_ism,))

        # Python bazadagi barcha mos kelgan qatorlarni o'ziga yuklab oladi
        natijalar = cursor.fetchall()

        if not natijalar:
            print(
                f"\n[!] Bazada '{qidirilayotgan_ism}' ismli birorta ham xodim topilmadi."
            )
        else:
            print(f"\n--- BAZADAN OLINGAN MA'LUMOTLAR ---")
            for xodim in natijalar:
                # xodim[0] = id, xodim[1] = ism, xodim[2] = familiya va h.k.
                print(
                    f"ID: {xodim[0]} | {xodim[1]} {xodim[2]} - {xodim[3]} | Maosh: ${xodim[4]}"
                )
            print("-----------------------------------")

    except Exception as error:
        print("Ma'lumot olishda xato:", error)
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    print("[*] Dastur ishga tushdi.")

    # Terminalda foydalanuvchidan ism so'raymiz
    user_input = input("\nBazadan qidirmoqchi bo'lgan ismingizni yozing: ")

    # Python shu ism bo'yicha bazaga borib ma'lumotni olib chiqadi
    bazadan_ism_boyicha_ol(user_input)
