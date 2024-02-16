from xml.etree.ElementTree import Element, SubElement, ElementTree

from jgb_editor.jeonggan import Page, TopPart, TitlePart, Gasaran, Gak, Gang, Jeonggan, Kan, Sumpyo, Sigimsae


class SaveJGBX:
    def __init__(self, pages: list[Page], gaks: int = 6, gangs: int = 4, jeonggans: int = 3):
        self.pages = pages
        self.gaks = gaks
        self.gangs = gangs
        self.jeonggans = jeonggans

    def save_xml(self, file_name: str):
        root = Element("jeongganbo")
        root.set("version", "1.0")

        title = self.pages[0].title_part.get_title()
        subtitle = self.pages[0].title_part.get_subtitle()

        if title is not None:
            root.set("title", title)
        else:
            root.set("title", "none")

        if subtitle is not None:
            root.set("subtitle", subtitle)
        else:
            root.set("subtitle", "none")

        for page in self.pages:
            page_xml = Element("page")
            root.append(page_xml)

            for gak in page.gaks_obj:
                gak_xml = Element("gak")
                page_xml.append(gak_xml)

                for gang in gak.gangs_obj:
                    gang_xml = Element("gang")
                    gak_xml.append(gang_xml)

                    tmp_gasaran = gang.get_gasaran()
                    tmp_sumpyo = tmp_gasaran.get_sumpyo_list()
                    tmp_sigimsae = tmp_gasaran.get_sigimsae_list()

                    for i in range(len(tmp_sumpyo)):
                        if tmp_sumpyo[i].label_type == "up" and tmp_sumpyo[i].is_enabled:
                            sumpyo_xml = Element("sumpyo")
                            sumpyo_xml.set("position", str(i))
                            gang_xml.append(sumpyo_xml)

                    for i in range(len(tmp_sigimsae)):
                        if tmp_sigimsae[i].label_type is not None:
                            sigimsae_xml = Element("sigimsae")
                            sigimsae_xml.set("position", str(i))
                            sigimsae_xml.set("type", tmp_sigimsae[i].label_type)
                            gang_xml.append(sigimsae_xml)

                    for jeonggan in gang.jeonggans_obj:
                        jeonggan_xml = Element("jeonggan")
                        gang_xml.append(jeonggan_xml)

                        for kan_row_i in range(len(jeonggan.rows_obj)):
                            kan_row_xml = Element("kan_row")
                            jeonggan_xml.append(kan_row_xml)

                            for kan in jeonggan.kans_obj[kan_row_i]:
                                kan_xml = Element("kan")

                                if kan.type == "note":  # note
                                    kan_xml.set("type", kan.type)
                                    kan_xml.set("note", kan.key)
                                    kan_xml.set("octave", str(kan.octave))
                                elif kan.type == "jangsikeum":  # jangsikeum
                                    kan_xml.set("type", kan.type)
                                    kan_xml.set("jangsikeum", kan.key)
                                else:  # None
                                    kan_xml.set("type", "none")
                                kan_row_xml.append(kan_xml)

        with open(file_name, "wb") as file:
            saved_xml = ElementTree(root)
            saved_xml.write(file, encoding='utf-8', xml_declaration=True)
