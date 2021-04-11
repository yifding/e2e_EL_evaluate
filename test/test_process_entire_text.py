from e2e_EL_evaluate.process_db_data.collect_pkl import process_entire_txt

#entire_txt = 'Later this week, <div style="background-color: yellow; display: inline;" id="qTvkuHQR4puo" data-annotation="https://en.wikipedia.org/wiki/Miami_Police_Department">Miami Police</div> apparently are going to escort them upto <div style="background-color: yellow; display: inline;" id="jfVnYMadqCXP" data-annotation="https://en.wikipedia.org/wiki/Tallahassee,_Florida">Tallahassee</div> and they will be ready to be counted if the judge decides at a later time to do so.   Now time is a big consideration from here. What\'s the judge\'s timetable?   Not as fast as the <div style="background-color: yellow; display: inline;" id="an5EM2ftTQiK" data-annotation="https://en.wikipedia.org/wiki/Democratic_Party_(United_States)">Democrats</div> would like, not as slowly as <div style="background-color: yellow; display: inline;" id="LtgR3WNiC2yj" data-annotation="https://en.wikipedia.org/wiki/Republican_Party_(United_States)">Republicans</div> would prefer.'
entire_txt = 'Habibi said the Iraqi and  <div style="background-color: yellow; display: inline;" id="3b6vjmFozz90" data-annotation="https://en.wikipedia.org/wiki/Palestinian_people">Palestinian</div>   questions were of great concern to Iran and Syria: "There should be coordination between the two countries over these issues.\'\' \n\n The official Iranian news agenc<div style="background-color: yellow; display: inline;" id="imJV4Gdtnx9I" data-annotation="lmao">y, IRMA, said the Iraqi and Palestinian issues would be the focus of talks between Habibi and Khaddam at the meeting of the Syrian-Iranian Supreme Committee.</div>'

txt, anno_list = process_entire_txt(entire_txt)
print('entire_txt:')
print(entire_txt)
print('processed_txt:')
print(txt)
print('anno_list', anno_list)
