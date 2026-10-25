# Fejlett robotprogramozás ROS környezetben - 5.1 Turtlesim Text Drawer

Sajnos a 3D szimulációs feladatokat nem bírta el a laptopom, így ezt tudtam megvalósítani. A program elindítja a Turtlesim ablakot, és kiírja a képernyőre a keresztnevemet: **ZSOLT**

## Funkciók
- **P-szabályozó alapú pályakövetés:** Szög- és távolsághiba alapú arányos sebességszabályozás holtidő és túllövés minimalizálással.
- **Relatív koordinátás vektorgrafikus betűkészlet**
- **Szervizkommunikáció (`SetPen`):** A toll dinamikus felemelése a betűközöknél, valamint betűnként eltérő RGB színek és vastagság használata.
- **Tiszta aszinkron állapotgép:** Timer alapú vezérlőhurok, non-blocking service hívásokkal.
- **ROS 2 Launch támogatás:** Egyetlen paranccsal indítható szimuláció és vezérlő.

## Futtatás
```bash
colcon build --packages-select turtlesim_text_drawer
source install/setup.bash
ros2 launch turtlesim_text_drawer drawer.launch.py
```