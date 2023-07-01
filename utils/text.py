def pc_text(data):
    body, cooler, drive, motherboard, processor, psu, ram, video_card, summ = data
    text = \
        f'Сборка ПК:\n' \
        f'<b>Процессор:</b> <code>{processor if processor != "none" else "-"}</code>\n' \
        f'<b>Корпус:</b> <code>{body if body != "none" else "-"}</code>\n' \
        f"<b>Кулер:</b> <code>{cooler if cooler != 'none' else '-'}</code>\n" \
        f'<b>Диск:</b> <code>{drive if drive != "none" else "-"}</code>\n' \
        f'<b>Материнская плата:</b> <code>{motherboard if motherboard != "none" else "-"}</code>\n' \
        f'<b>Блок питания:</b> <code>{psu if psu != "none" else "-"}</code>\n' \
        f'<b>Оперативная память:</b> <code>{ram if ram != "none" else "-"}</code>\n' \
        f'<b>Видеокарта:</b> <code>{video_card if video_card != "none" else "-"}</code>\n' \
        f'Стоимость: {"{0:,}".format(summ).replace(",", " ")}₽'
    return text

