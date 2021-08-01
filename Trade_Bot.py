# импорт модулей
from vk_api.longpoll import *
from array import *
import vk_api, time, datetime, re

# хелло ворлд
tmpTime = time.strftime('%H:%M:%S')
print(tmpTime, "TraderBot был успешно запущен...\n")

# логинимся
tmpVkSession = vk_api.VkApi(token="Токен_с_правами_Message_и_Offline")
tmpLongpoll = VkLongPoll(tmpVkSession)

# что скупить
tmpItems = dict()
#книги
tmpItems["мощный удар"] = array('i', [4000, 50])
tmpItems["раскол"] = array('i', [4000, 50])
tmpItems["феникс"] = array('i', [2500, 50])
#tmpItems["камень"] = array('i', [50, 5])
# первичка
tmpItems["лен"] = array('i', [50, 5])
tmpItems["железная руда"] = array('i', [50, 5])
tmpItems["бревно"] = array('i', [50, 5])
tmpItems["камень"] = array('i', [50, 5])
# вторичка
tmpItems["каменный блок"] = array('i', [50, 5])
tmpItems["доска"] = array('i', [50, 5])
tmpItems["железный слиток"] = array('i', [50, 5])
tmpItems["ткань"] = array('i', [50, 5])
# ресурсы
tmpItems["пещерный корень"] = array('i', [40, 5])
#tmpItems["рыбий жир"] = array('i', [50, 5])
tmpItems["камнецвет"] = array('i', [50, 5])
tmpItems["адский гриб"] = array('i', [50, 5])
tmpItems["адский корень"] = array('i', [50, 5])
tmpItems["чистая первозданная вода"] = array('i', [50, 5])
tmpItems["болотник"] = array('i', [200, 5])
tmpItems["кровавый гриб"] = array('i', [50, 5])
tmpItems["необычный цветок"] = array('i', [50, 5])
tmpItems["сквернолист"] = array('i', [50, 5])
tmpItems["чернильник"] = array('i', [50, 5])
tmpItems["корень знаний"] = array('i', [50, 5])
tmpItems["сверкающая чешуя"] = array('i', [50, 5])
tmpItems["рыбий глаз"] = array('i', [50, 5])
tmpItems["ракушка"] = array('i', [50, 5])

# сообщение
def send(event, partition, name, quantity, cost):
    tmpVkSession.method('messages.send', {'peer_id': -182985865,
                                        'message': str(partition),
                                        'random_id': 0,
                                        'forward_message': time.sleep(0.000001)})
    tmpTime = time.strftime('%H:%M:%S')
    print("[%s] Пытаемся купить %d %s за %d" % (tmpTime, quantity, name, cost * quantity))

# покупка товара
def buy(event, partition, items):
    tmpNumbers = re.search(r'(\d+)\*(.+?) - (\d+)', partition)
    tmpName = tmpNumbers[2]
    if (tmpName in items):
        tmpItem = items[tmpName]
        tmpQuantity = int(tmpNumbers[1])
        if (int(tmpItem[1]) - tmpQuantity >= 0):
            tmpPrice = int(tmpNumbers[3])
            tmpCost = tmpPrice / tmpQuantity
            if (tmpCost <= tmpItem[0]):
                send(event, partition, tmpName, tmpQuantity, tmpCost)

# учет покупки
def save(event, partition, items):
    tmpNumbers = re.search(r'(\d+)\*(.+?) - (\d+)', partition)
    tmpName = tmpNumbers[2]
    if (tmpName in items):
        tmpItem = items[tmpName]
        tmpQuantity = int(tmpNumbers[1])
        tmpItem[1] = int(tmpItem[1]) - tmpQuantity
        print("--> УСПЕХ! %d %s куплено, осталось купить %d" % (tmpQuantity, tmpName, tmpItem[1]))

#buy(0, "1*рыбий жир - 20 золота потрачено!", tmpItems)
#save(0, "⚖Вы успешно приобрели с аукциона предмет 1*рыбий жир - 99 золота потрачено!", tmpItems)
#raise SystemExit

while True:
    try:
        time.sleep(1)
        for event in tmpLongpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                text = event.text.lower()
                # лот создает смотритель
                if hasattr(event, "user_id"):
                    if event.user_id == -183040898:
                        partition = text.partition("\n")
                        if (("выставляет ") in partition[0]):
                            buy(event, partition[2], tmpItems)
                # в личку пишет колодец
                if event.peer_id == -182985865:
                    if (("вы успешно приобрели ") in text):
                        save(event, text, tmpItems)
    except Exception as e:
        print(e)
        pass
