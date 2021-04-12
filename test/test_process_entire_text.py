import re
import html
# from e2e_EL_evaluate.process_db_data.collect_pkl import process_entire_txt

#entire_txt = 'Later this week, <div style="background-color: yellow; display: inline;" id="qTvkuHQR4puo" data-annotation="https://en.wikipedia.org/wiki/Miami_Police_Department">Miami Police</div> apparently are going to escort them upto <div style="background-color: yellow; display: inline;" id="jfVnYMadqCXP" data-annotation="https://en.wikipedia.org/wiki/Tallahassee,_Florida">Tallahassee</div> and they will be ready to be counted if the judge decides at a later time to do so.   Now time is a big consideration from here. What\'s the judge\'s timetable?   Not as fast as the <div style="background-color: yellow; display: inline;" id="an5EM2ftTQiK" data-annotation="https://en.wikipedia.org/wiki/Democratic_Party_(United_States)">Democrats</div> would like, not as slowly as <div style="background-color: yellow; display: inline;" id="LtgR3WNiC2yj" data-annotation="https://en.wikipedia.org/wiki/Republican_Party_(United_States)">Republicans</div> would prefer.'
#
# entire_txt = 'Later this week, ' \
#              '<div style="background-color: yellow; display: inline;" id="qTvkuHQR4puo" data-annotation="https://en.wikipedia.org/wiki/Miami_Police_Department">Miami Police</div> ' \
#              'apparently are going to escort them upto ' \
#              '<div style="background-color: yellow; display: inline;" id="jfVnYMadqCXP" data-annotation="https://en.wikipedia.org/wiki/Tallahassee,_Florida">Tallahassee</div> ' \
#              'and they will be ready to be counted if the judge decides at a later time to do so.   Now time is a big consideration from here. What\'s the judge\'s timetable?   Not as fast as the ' \
#              '<div style="background-color: yellow; display: inline;" id="an5EM2ftTQiK" data-annotation="https://en.wikipedia.org/wiki/Democratic_Party_(United_States)">Democrats</div> ' \
#              'would like, not as slowly as ' \
#              '<div style="background-color: yellow; display: inline;" id="LtgR3WNiC2yj" data-annotation="https://en.wikipedia.org/wiki/Republican_Party_(United_States)">Republicans</div> ' \
#              'would prefer.'


# problem 3/117 errors
entire_txt = '<div style="background-color: yellow; display: inline;" id="beA9OuKiTQ5W" data-annotation="https://en.wikipedia.org/wiki/Anthony_Grant"><div style="background-color: yellow; display: inline;" id="yWOq1WevGL1h" data-annotation="https://en.wikipedia.org/wiki/Anthony_Grant">Anthony Grant</div></div>,'
# entire_txt = 'VCU hired Smart to be the head coach in the spring of 2009 after the program\'s previous coach, <div style="background-color: yellow; display: inline;" id="beA9OuKiTQ5W" data-annotation="https://en.wikipedia.org/wiki/Anthony_Grant"><div style="background-color: yellow; display: inline;" id="yWOq1WevGL1h" data-annotation="https://en.wikipedia.org/wiki/Anthony_Grant">Anthony Grant</div></div>, left to become the head coach of the <div style="background-color: yellow; display: inline;" id="rgOC9f10bR6X" data-annotation="https://en.wikipedia.org/wiki/Alabama_Crimson_Tide_men%27s_basketball">Alabama Crimson Tide men\'s basketball team</div>. Smart\'s hire made him the 10th-youngest head coach in Division I. In <div style="background-color: yellow; display: inline;" id="S82akw3SIevW" data-annotation="https://en.wikipedia.org/wiki/2009%E2%80%9310_Alabama_Crimson_Tide_men%27s_basketball_team">his first season</div>, he led the Rams to a 27–10 season and a <div style="background-color: yellow; display: inline;" id="vNO4xst0Jzn3" data-annotation="https://en.wikipedia.org/wiki/2010_College_Basketball_Invitational">CBI Championship</div> after VCU swept <div style="background-color: yellow; display: inline;" id="0MHsjDbfx2Lb" data-annotation="https://en.wikipedia.org/wiki/2009%E2%80%9310_Saint_Louis_Billikens_men%27s_basketball_team">Saint Louis</div> in the championship best-of-three series.'
# entire_txt = '<div style="background-color: yellow; display: inline;" id="buUpwjyD83h4" data-annotation="https://en.wikipedia.org/wiki/University_of_Chester">Services\nChester Business School\nResearch\nTheology</div> and Religious Studies MainOur Courses\nStaff Research\nNews and Events\nStaff\nStudents\nAboutOutreach\nSocial Responsibility\nAbout the University\nPress Office\nAlumni\nWho to Contact\nFlash Fiction MagazineFlash Adverts\nFlash Bibliography\nFlash Links\nFlash '
# entire_txt = '<div style="background-color: yellow; display: inline;" id="LbGT8OOc5GBG" data-annotation="https://en.wikipedia.org/wiki/National_Basketball_Association">NBA</div> BASKETBALL - STANDINGS AFTER THURSDAY \'S GAMES.\n<div style="background-color: yellow; display: inline;" id="Z1AFK2SVzWOO" data-annotation="https://en.wikipedia.org/wiki/New_York">NEW YORK</div> 1996-12-06\nStandings of <div style="background-color: yellow; display: inline;" id="wplx4X6aVSAQ" data-annotation="https://en.wikipedia.org/wiki/National_Basketball_Association">National Basketball Association</div> teams after games played on Thursday\n( tabulate under won, lost, percentage, games behind ):<div style="background-color: yellow; display: inline;" id="bMG1KAQ05SZ8" data-annotation="https://en.wikipedia.org/wiki/Eastern_Conference_(NBA)">\nEASTERN CONFERENCE</div>\n<div style="background-color: yellow; display: inline;" id="XwVn6qVS5Pin" data-annotation="https://en.wikipedia.org/wiki/Atlantic_Division_(NBA)">ATLANTIC </div><div style="background-color: yellow; display: inline;" id="zKd3W2EMMyso" data-annotation="https://en.wikipedia.org/wiki/Atlantic_Division_(NBA)">DIVISION</div>\nW L PCT GB\n<div style="background-color: yellow; display: inline;" id="xib2LGHxihzA" data-annotation="https://en.wikipedia.org/wiki/Miami_(disambiguation)">MIAMI</div> 14 4 .778 -\n<div style="background-color: yellow; display: inline;" id="zePsl72jMYFr" data-annotation="https://en.wikipedia.org/wiki/New_York_Knicks">NEW YORK</div> 10 6 .625 3\n<div style="background-color: yellow; display: inline;" id="8sljPiGNgstn" data-annotation="https://en.wikipedia.org/wiki/Orlando_Magic">ORLANDO</div> 8 6 .571 4\n<div style="background-color: yellow; display: inline;" id="hUHgK2opuMCG" data-annotation="https://en.wikipedia.org/wiki/Washington_Wizards">WASHINGTON</div> 7 9 .438 6\n<div style="background-color: yellow; display: inline;" id="GDgw8AdTdUsv" data-annotation="https://en.wikipedia.org/wiki/Philadelphia_76ers">PHILADELPHIA</div> 7'

def process_entire_txt(entire_txt):
    """
    Core function to process the labelled text to obtain, use regular expression to extract.
    :param entire_txt: raw text with potential annotated entities.

    '<div style="background-color: yellow; display: inline;" id="1ZeqcTpSxhSG" data-annotation="https://en.wikipedia.org/wiki/Germany">German</div>

    :return: (txt, anno_list) tuple,
    txt: raw text without entity annotations
    anno_list: a list of annotations (dictionary)
    """

    def process(s):
        return html.unescape(s)

    def extract(s):
        """
        :param s: r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="(.+)">(.+)</div>'
        :return: mention, entity

        txt: plain txt without annotations.
        """

        wiki_prefix = 'https://en.wikipedia.org/wiki/'
        pre = 'data-annotation="'
        mid = '">'
        post = '</div>'

        if
        pre_pos = s.find(pre)
        mid_pos = s.find(mid)
        post_pos = s.find(post)
        assert 0 < pre_pos < mid_pos < post_pos

        mention = s[mid_pos + len(mid): post_pos]
        entity = s[pre_pos + len(pre): mid_pos]
        print(s)
        print('\n')
        # print('mention', mention)
        # print('entity', entity)
        # print('\n')
        if entity.startswith(wiki_prefix):
            entity = entity[len(wiki_prefix):]
        else:
            entity = ''

        return mention, entity

    entire_txt = process(entire_txt)
    txt = ''
    anno_list = []
    cur_pos = 0

    r_s = r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="([\s\S]*?)">([\s\S]*?)</div>'
    # **YD** enhenced version of regular expression matching pattern.
    # r_s = r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="(((?!<div)(?!</div>).)+)</div>'

    for i in re.finditer(r_s, entire_txt):
        start = i.start()
        end = i.end()
        # print('captured annotations!')
        # print(entire_txt[start:end])
        # print('\n')
        txt += entire_txt[cur_pos: start]
        cur_pos = end

        mention, entity = extract(entire_txt[start: end])

        if entity != '':
            anno_list.append(
                {
                    'start': len(txt),
                    'end': len(txt) + len(mention),
                    'mention_txt': mention,
                    'entity_txt': entity,
                }
            )
        txt += mention

    txt += entire_txt[cur_pos:]

    return txt, anno_list


txt, anno_list = process_entire_txt(entire_txt)
print('entire_txt:')
print(entire_txt)
print('processed_txt:')
print(txt)
print('anno_list', anno_list)
