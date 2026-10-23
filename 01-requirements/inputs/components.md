# Components (transcribed from the pictures sent 2026-10-19)

Values marked **(drawing)** are read from a dimensioned drawing. **(photo)** = from a product photo with dimension arrows.
**(assumed)** = not in the material, typical value. Must be confirmed or measured, and becomes a parameter.

## C1: 4-channel relay module (main relay board). Picture: [component-C1-relay-board.png](component-C1-relay-board.png)
- 4 × SONGLE **SRD-05VDC-SL-C** relays, rated **10 A 250 VAC / 10 A 30 VDC**. High/low-level trigger jumpers.
- Screw terminals: control (DC+, DC−, IN1–IN4) on one long edge; NO/COM/NC per relay on the other long edge.
- 4 corner mounting holes.
- **Measured (I10):** PCB **75 × 52 mm**, holes **70 × 46 mm** centre to centre, **Ø3 mm**, height **17 mm** (PCB underside → relay tops), solder pins **3 mm** below the PCB.

## C2: USB-C PD power adapter, model **ZQ-P3020C** ("PD Charger"). Picture: [component-C2-usb-c-adapter.png](component-C2-usb-c-adapter.png)
- Input 100–240 V~ 50/60 Hz 0.8 A. Output USB-C PD max 30 W (5 V 3 A, 9 V 3 A, 12 V 2.5 A, 15 V 2 A, 20 V 1.5 A).
- Size **50 × 49 × 27 mm (photo)**. Flying mains leads (brown/blue) with WAGO 221 connectors. One through-hole lug for a screw on top.
- Made for mounting inside a wall/junction box.
- From the photo: the **USB-C port** is on a 50 × 49 face (near one edge, centred). The **mains leads** come out of a 49 × 27 side face. The mounting hole sits near the top-right corner of the port face and appears to run through the 27 mm depth. **Measured (I10):** size **51 (cable side) × 49 × 27 mm** at the bottom; hole goes through, **Ø3.5**, centre **3.5 mm** from the top edge and **8 mm** from the side opposite the cable; **~5 mm recess** on the port side (screw in the hole for 22 mm).

## C3: 3.5 mm panel-mount jack socket (temperature sensor). Picture: [component-C3-jack-socket.png](component-C3-jack-socket.png)
- Overall length **20 mm**, front part **10 mm**, jack opening **3.5 mm (photo)**. Solder lugs at the back.
- Black round front nut Ø ≈ 10 mm (with the 3.5 mm opening), silver hex nut behind it. The wall is clamped between the two nuts **(photo)**.
- **Measured (I10):** thread **M8**, usable thread length **4 mm**, hex nut **2 mm** thick / **11 mm** widest, front nose **Ø10 mm**.

## C4: IEC C14 power inlet with fuse holder, screw mount. Picture: [component-C4-iec-inlet.png](component-C4-iec-inlet.png)
- Flange **43.8 × 32.8 mm**, flange thickness **3.1 mm**, 2 mounting holes **Ø3.5** at **36.0 mm** spacing **(drawing)**.
- Body behind the flange **27 × 31.0 mm**, front face 27 × 30.8 with corner radius r4 **(drawing)**.
- Depth behind the panel **27.6 mm** (19.5 body + lugs), lugs: N, PE (earth), L, fuse **(drawing)**.
- Rated **10 A 250 V~**.
- Panel cutout ≈ 27.5 × 31.5 mm with corner radius ≈ 4 mm **(derived)**.

## C5: Panel-mount earthed power socket (Schuko type), 16 A, 2P+E, with hinged cover. Picture: [component-C5-power-socket.png](component-C5-power-socket.png)
Manufacturer drawing (St. Martin im Innkreis, Austria), 1:1 table:

| Dim | Meaning | mm |
|---|---|---|
| a | square flange | **50** |
| b | mounting-hole square | **38** |
| c | total height incl. hinged cover | **62** |
| d | cover hinge width | **25** |
| e | depth in front of the panel | **21** |
| f | depth behind the panel | **26** |
| g | body Ø = panel cutout | **43** |
| h | mounting holes | **Ø4.5** (M4) |

## C6: Rocker switch, 2-position I/0, illuminated, splash-proof boot (main switch). Picture: [component-C6-rocker-switch-2pos.png](component-C6-rocker-switch-2pos.png)
- Front bezel **35.3 × 29 mm** incl. rubber boot (boot 22.4 wide), bezel height **4 mm** **(drawing)**. **Measured (I10):** plastic frame **25.5 × 34.5 mm**, clip gap (bezel underside → clip tip) **4 mm**.
- Body **26 × 21.7 mm**, depth **15.1 mm** + terminals **10.2 mm** (6.3 mm tabs), 4 pins **(drawing)**. **Measured (I10):** body **21 × 25 mm**, **34 mm** across the clips.
- **Panel cutout 27 × 22 mm** **(drawing)**. Snap-in clips.

## C7: Rocker switch, 3-position I/0/II, illuminated, splash-proof boot (boiler + pump, 2 ×). Picture: [component-C7-rocker-switch-3pos.png](component-C7-rocker-switch-3pos.png)
- Front bezel **35 mm** long (rocker 25.5) **(drawing)**. **Measured (I10):** plastic frame **25.7 × 34.5 mm**, clip gap **3 mm**, body **21.5 × 27 mm**, **33 mm** across the clips.
- Total height incl. terminals **40.5 mm**, terminal length 9.5 mm, 6 pins **(drawing)**.
- **Panel cutout 28.5 × 21.5 mm** **(drawing)**. Snap-in clips.

## C8: Raspberry Pi (not pictured, public data)
- Pi 3B/3B+, Pi 4B and Pi 5 share the same board outline **85 × 56 mm** and mounting holes **58 × 49 mm**, **Ø2.75 mm (M2.5)**, 3.5 mm from the board edges.
- Port layout differs: Pi 3 has micro-USB power; Pi 4/5 have USB-C and 2 × micro-HDMI; Pi 5 swaps the USB/Ethernet positions. Pi 5 needs active cooling under load.
