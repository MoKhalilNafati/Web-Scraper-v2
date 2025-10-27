import asyncio
import aiohttp
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.daad.de/en/studying-in-germany/universities/all-degree-programmes/?hec-degreeProgrammeType=w&hec-teachingLanguage=2&hec-subjectGroup=2-226,2-229,2-232,2-233,2-234,2-235,2-404,2-547,2-548,2-236&hec-deadlineId=3&hec-studyType=t,v&hec-limit=100&hec-admissionMode=O,X"

# ----------------------
# Helper: fetch page
# ----------------------
async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()

# ----------------------
# Parse detail page
# ----------------------
def parse_detail_page(html):
    soup = BeautifulSoup(html, "lxml")

    # area of study
    h5_aos = soup.find("h5", string="Area of study")
    if h5_aos:
        ul = h5_aos.find_next_sibling("ul")
        if ul:
            aos = " | ".join(li.text.strip() for li in ul.find_all("li"))
        else:
            p = h5_aos.find_next_sibling("p")
            aos = p.text.strip() if p else "-"
    else:
        aos = "-"

    # focus
    h5_focus = soup.find("h5", string="Focus")
    focus = h5_focus.find_next_sibling("p").text.strip() if h5_focus and h5_focus.find_next_sibling("p") else "-"

    # deadlines
    ddln = soup.find_all("h6", string="Deadlines for international students from countries that are not members of the European Union")
    deadlines = " | ".join(d.find_next_sibling("p").text.strip() for d in ddln) if ddln else "-"

    # admission semester
    h5_semester = soup.find("h5", string="Admission semester")
    semester = h5_semester.find_next_sibling("p").text.strip() if h5_semester and h5_semester.find_next_sibling("p") else "-"

    # annotation
    h5_annotation = soup.find("h5", string="Annotation")
    annotation = h5_annotation.find_next_sibling("p").text.strip() if h5_annotation and h5_annotation.find_next_sibling("p") else "-"

    # admission modus
    h5_modus = soup.find("h5", string="Admission modus")
    if h5_modus:
        ps = h5_modus.find_next_siblings("p")
        if len(ps) > 1:
            text_part = ps[0].text.strip()
            a_tag = ps[1].find("a")
            link_part = a_tag["href"] if a_tag and a_tag.has_attr("href") else "-"
            modus = text_part + " | " + link_part
        elif len(ps) == 1:
            modus = ps[0].text.strip()
        else:
            modus = "-"
    else:
        modus = "-"

    # admission requirements
    h5_requirements = soup.find("h5", string="Admission requirements")
    requirements = h5_requirements.find_next_sibling("p").text.strip() if h5_requirements and h5_requirements.find_next_sibling("p") else "-"

    # lecture period
    h5_lecture = soup.find("h5", string="Lecture period")
    if h5_lecture:
        ul = h5_lecture.find_next_sibling("ul")
        if ul:
            lecture = " | ".join(li.text.strip() for li in ul.find_all("li"))
        else:
            p = h5_lecture.find_next_sibling("p")
            lecture = p.text.strip() if p else "-"
    else:
        lecture = "-"

    #Find Student advisory service
    h4_section = soup.find("h4", string="Student advisory service")
    email = "-"
    web = "-"

    if h4_section:
        div_item = h4_section.find_next_sibling("div")
        if div_item:
            dls = div_item.find_all("dl")
            i = 0
            while i < len(dls):
                dl = dls[i]
                dt_email = dl.find("dt", string="E-Mail:")
                if dt_email:
                    dd_email = dt_email.find_next_sibling("dd")
                    if dd_email:
                        span_email = dd_email.find("span", class_="link__text u-decoration-underline")
                        if span_email:
                            raw_email = span_email.get_text(separator="", strip=True)
                            email = raw_email.replace(' at ', '@').replace(' ','')

                dt_web = dl.find("dt", string="Web:")
                if dt_web:
                    dd_web = dt_web.find_next_sibling("dd")
                    if dd_web:
                        a_web = dd_web.find("a")
                        if a_web and a_web.has_attr("href"):
                            web = a_web["href"]

                if email != "-" and web != "-":
                    break
                i += 1

    advisory = email + " | " + web

    return aos, focus, deadlines, semester, annotation, modus, requirements, lecture, advisory

# ----------------------
# Main async logic
# ----------------------
async def main():
    async with aiohttp.ClientSession() as session:
        # Fetch main listing page
        html = await fetch(session, BASE_URL)
        soup = BeautifulSoup(html, "lxml")

        programs = [p.text.strip() for p in soup.select("span.result__headline-content.mb-24")]
        universities = [u.text.strip() for u in soup.select("span.result__headline-content.mb-8")]

        # locations
        locations = [dd.text.strip() for dd in soup.select("dt:-soup-contains('Location:') + dd")
]
        # period of study
        periods = [dd.text.strip() for dd in soup.select("dt:-soup-contains('Standard Period of Study:') + dd")]


        # detail links
        links = ["https://www.daad.de" + a["href"] for a in soup.select("a.qa-more-link")]

        # Fetch all detail pages in parallel
        detail_htmls = await asyncio.gather(*(fetch(session, link) for link in links))

        results = []
        for i, page in enumerate(detail_htmls):
            aos, focus, deadlines, semester, annotation, modus, requirements, lecture, advisory = parse_detail_page(page)
            results.append([
                programs[i], universities[i], locations[i], periods[i],
                aos, focus, deadlines, semester, annotation, modus, requirements, lecture, advisory, links[i]
            ])

        # Save to CSV
        with open("C:/Users/Khalil/Documents/VS/Web Scraping v2/programs.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Program", "University/Hochschule", "Location", "Period Of Study",
                "Area Of Study", "Focus", "Deadlines", "Admission Semester",
                "Annotation", "Admission Modus", "Admission requirements", "Lecture period", "Find Student advisory service", "Links"
            ])
            writer.writerows(results)

# Run async program
asyncio.run(main())
