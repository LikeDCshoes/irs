from lxml.html import fromstring
import requests
import os


class Form:
    def __init__(self, number, title, revisions=None):
        self.number = number
        self.title = title
        self.revisions = revisions if revisions is not None else []

    class Revision:
        def __init__(self, year, link):
            self.year = year
            self.link = link

    def add_revision(self, year, link):
        self.revisions.append(self.Revision(year, link))

    def get_min_year(self):
        return min([revision.year for revision in self.revisions]) if self.revisions else None

    def get_max_year(self):
        return max([revision.year for revision in self.revisions]) if self.revisions else None


def get_form(form_name, max_requests=100, extra_params=None):
    """
    :param form_name: Exact name of form to search.
    :param max_requests: Quantity of maximum requests to remote allowed to do.
    :param extra_params: Additional parameters for requests to remote.
    :return: Instance of class "Form".
    """

    base_url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html'

    base_params = {
        'sortColumn': 'sortOrder',
        'resultsPerPage': 200,
        'isDescending': 'false',
        'criteria': 'formNumber',
        'indexOfFirstRow': 0,
        'value': ''
    }

    params = base_params.copy()
    if extra_params is None:
        extra_params = {}
    params.update(extra_params)
    params['value'] = form_name

    form_instance = None
    has_next = True
    iteration = 0
    while has_next and iteration <= max_requests:
        try:
            resp = requests.get(base_url, params=params, timeout=10)
        except requests.exceptions.Timeout:
            # If timeout has occurred, try again the same request.
            continue
        finally:
            iteration += 1

        if resp.status_code != requests.codes.ok:
            # FIXME: Maybe need some other behavior.
            break

        doc = fromstring(resp.text)

        # First row is table header. Skip it by "[1:]".
        for tr in doc.xpath('//div[@class="picklistTable"]//tr')[1:]:
            number = tr.xpath('.//td[@class="LeftCellSpacer"]/a')[0].text_content().strip()
            if number != form_name:
                continue

            title = tr.xpath('.//td[@class="MiddleCellSpacer"]')[0].text_content().strip()
            year = int(tr.xpath('.//td[@class="EndCellSpacer"]')[0].text_content().strip())
            link = tr.xpath('.//td[@class="LeftCellSpacer"]/a')[0].attrib['href']

            if not form_instance:
                form_instance = Form(number=number, title=title)

            form_instance.add_revision(year=year, link=link)

        params['indexOfFirstRow'] += params['resultsPerPage']

        # To define, if there another page for this search query.
        if not doc.xpath('//th[@class="NumPageViewed"]/b') or doc.xpath('//th[@class="NumPageViewed"]/b')[0].getnext() is None:
            has_next = False

    return form_instance


def download_form(form_name, year_from=None, year_to=None):
    """

    :param form_name: Exact name of form to search.
    :param year_from: Min year of form to download.
    :param year_to: Max year of form to download.
    :return:
    """
    form = get_form(form_name)

    if not form:
        print('There are no forms with name "%s".' % form_name)
        return 0

    files_counter = 0
    for revision in form.revisions:
        if year_from and revision.year < year_from:
            continue
        if year_to and revision.year > year_to:
            continue

        if not os.path.exists(form.number):
            os.mkdir(form.number)

        try:
            print('Downloading %s for %s...' % (form.number, revision.year))
            resp = requests.get(revision.link, timeout=10)
        except requests.exceptions.Timeout:
            # FIXME: Maybe need some other behavior.
            continue

        filename, extension = os.path.splitext(revision.link)
        with open(os.path.join(form_name, '%s-%s%s' % (form_name, revision.year, extension)), 'wb') as f:
            f.write(resp.content)
            files_counter += 1

    return files_counter
