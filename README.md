# Turtlesim Text Drawer - Fejlett robotprogramozás ROS környezetben

Kötelező program megvalósítás az 5.1 (Turtlesim Fraktál/Szöveg) témakörben (Epic szint).

## Funkciók
- **P-szabályozó alapú pályakövetés:** Szög- és távolsághiba alapú proporcionális sebességszabályozás holtidő és túllövés minimalizálással.
- **Tetszőleges szöveg rajzolása:** Relatív koordinátás vektorgrafikus betűkészlet (pl. ROS 2 felirat).
- **Szervizkommunikáció (`SetPen`):** A toll dinamikus felemelése a betűközöknél, valamint betűnként eltérő RGB színek és vastagság használata.
- **Tiszta aszinkron állapotgép:** Timer alapú vezérlőhurok, non-blocking szervizhívásokkal.
- **ROS 2 Launch támogatás:** Egyetlen paranccsal indítható szimuláció és vezérlő.

## Futtatás
```bash
colcon build --packages-select turtlesim_text_drawer
source install/setup.bash
ros2 launch turtlesim_text_drawer drawer.launch.py
```

## Egyedi szöveg megadása launch paraméterrel:
```bash
ros2 launch turtlesim_text_drawer drawer.launch.py text_to_draw:="ROS 2" scale:=1.4
```