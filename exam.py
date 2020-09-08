balls = [1, 2, 3, 4]
weapons = [11, 22, 3, 44]

for ball_idx, ball_val in enumerate(balls):
    print("Ball : ", ball_val)
    for weapon_idx, weapon_val in enumerate(weapons):
        print("Weapons:", weapon_val)
        if ball_val == weapon_val:
            print("충돌")
            break
        # 브레이크로 for문 탈출을 원했으나 2중 for문이므로 내부 for문만 탈출
        # 즉, 외부 for문 때문에 코드가 멈추지 않고 실행이 되는 현상이 발생

    else:  # for문에 값이 없다면 else 구문으로 넘어옴
        continue  # continue 사용으로 값이 없다면 바깥쪽 for문을 진행
    break  # 외부 for문 종료
