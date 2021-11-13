
# layer 0: Background Objects
# layer 1: Foreground Objects
objects = [[],[]]
# 게임 월드는 객체들의 집합 -> 리스트로 표현
# 객체들의 깊이를 주기 위해 깊이 레이어 구분
# 레이어 낮은 게 먼저 그려진다

def add_object(o, layer):
    objects[layer].append(o)


def add_objects(l, layer):
    objects[layer] += l # 리스트를 넘겨줌


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break




def clear():
    for o in all_objects():
        del o
    for l in objects:
        l.clear()

def destroy():
    clear()
    objects.clear()


def all_objects():  # 제너레이터
    for i in range(len(objects)):
        for o in objects[i]:
            yield o

# for 문과 함께 쓰게 되면
# 단독으로는 못 쓴다
# 제너레이터는 일드 시점에서 함수 호출이 끝나고 반환 (마지막에 반환하는 일반 함수들과 다름)

