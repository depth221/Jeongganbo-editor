import xml.etree.ElementTree as ET

from PyQt5.QtWidgets import QMainWindow, QGridLayout

from jgb_editor.jeonggan import Page, TopPart, TitlePart, Gasaran, Gak, Gang, Jeonggan, Kan, Sumpyo, Sigimsae


class LoadJGBX:
    def __init__(self, file_path: str, window_obj: QMainWindow, pages_obj: list[Page]):
        self.file_path = file_path
        self.pages_obj = pages_obj
        self.pages_obj.clear()
        self.window_obj = window_obj

        try:
            self.file_xml = ET.parse(self.file_path)
        except Exception:
            raise Exception(f"{self.load_xml.__name__}: "
                            f"파일의 경로가 잘못되었습니다({self.file_path}).")

    def load_xml(self) -> tuple[int, int, int]:
        file_xml = self.file_xml

        root = file_xml.getroot()
        title: str = root.attrib["title"]
        subtitle: str = root.attrib["subtitle"]

        page_num = 0
        for _ in root:
            page_num += 1

        page_count = 0
        for page_xml in root:
            gak_num = 0
            gang_num = 0
            jeonggan_num = 0
            for gak_iter in page_xml:
                if gak_num == 0:
                    for gang_iter in gak_iter:
                        if gang_num == 0:
                            for jeonggan_item in gang_iter:
                                if jeonggan_item.tag == "jeonggan":
                                    jeonggan_num += 1
                        gang_num += 1
                gak_num += 1

            page = Page(gak_num, gang_num, jeonggan_num, title=(page_count == 0), _id=page_count,
                        parent=self.window_obj)
            if page_count == 0:
                page.title_part.title = title
                page.title_part.subtitle = subtitle
                page.title_part.convert_vertical_rl()

            self.pages_obj.append(page)

            gak_count = 0
            for gak_xml in page_xml:
                curr_gak: Gak = page.gaks_obj[gak_count]

                gang_count = 0
                for gang_xml in gak_xml:
                    curr_gang: Gang = curr_gak.gangs_obj[gang_count]

                    jeonggan_count = 0
                    for sub_gang_item in gang_xml:
                        curr_jeonggan: Jeonggan = curr_gang.jeonggans_obj[jeonggan_count]

                        if sub_gang_item.tag == "sumpyo":
                            curr_gang.gasaran.sumpyos[int(sub_gang_item.attrib["position"])].click()
                        elif sub_gang_item.tag == "sigimsae":
                            curr_gang.gasaran.sigimsaes[int(sub_gang_item.attrib["position"])].label_type \
                                = sub_gang_item.attrib["type"]
                            curr_gang.gasaran.sigimsaes[int(sub_gang_item.attrib["position"])].set_sigimsae(
                                curr_gang.gasaran.sigimsaes[int(sub_gang_item.attrib["position"])]
                            )
                        elif sub_gang_item.tag == "jeonggan":
                            kan_row_num = 0
                            kan_col_num = 0
                            for sub_gang_iter in sub_gang_item:
                                if kan_row_num == 0:
                                    for _ in sub_gang_iter:
                                        kan_col_num += 1
                                kan_row_num += 1

                            kan_row_count = 0
                            for kan_row_xml in sub_gang_item:
                                if kan_row_count >= 3:  # malformed save file
                                    break

                                if kan_row_count != 0:
                                    curr_jeonggan.append_row()

                                kan_col_count = 0
                                for kan_xml in kan_row_xml:
                                    if kan_col_count >= 3:  # malformed save file
                                        break

                                    if kan_col_count != 0:
                                        curr_jeonggan.append(kan_row_count)

                                    curr_kan: Kan = curr_jeonggan.kans_obj[kan_row_count][kan_col_count]
                                    kan_type: str = kan_xml.attrib["type"]

                                    if kan_type == "note":
                                        curr_kan.set_note(kan_xml.attrib["note"], int(kan_xml.attrib["octave"]))
                                    elif kan_type == "jangsikeum":
                                        curr_kan.set_jangsikeun(kan_xml.attrib["jangsikeum"])
                                    elif kan_type == "none":
                                        curr_kan.clear_all()
                                    else:
                                        print(f"{self.load_xml.__name__}: 'kan' 아래에 'note', 'jangsikeum', 'none' "
                                              f" 이외의 요소가 존재합니다({kan_type}).")

                                    kan_col_count += 1

                                kan_row_count += 1

                            jeonggan_count += 1
                        else:
                            print(f"{self.load_xml.__name__}: 'gang' 아래에 'sumpyo', 'sigimsae', 'jeonggan' "
                                  f" 이외의 요소가 존재합니다({sub_gang_item.tag}).")

                    gang_count += 1

                gak_count += 1

            page_count += 1

        return (6 if gak_num is None else gak_num,
                4 if gang_num is None else gang_num,
                3 if jeonggan_num is None else jeonggan_num)
