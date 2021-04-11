import re

### test for doc_anno
entire_txt = 'Habibi said the Iraqi and  <div style="background-color: yellow; display: inline;" id="3b6vjmFozz90" data-annotation="https://en.wikipedia.org/wiki/Palestinian_people">Palestinian</div>   questions were of great concern to Iran and Syria: "There should be coordination between the two countries over these issues.\'\' \n\n The official Iranian news agenc<div style="background-color: yellow; display: inline;" id="imJV4Gdtnx9I" data-annotation="lmao">y, IRMA, said the Iraqi and Palestinian issues would be the focus of talks between Habibi and Khaddam at the meeting of the Syrian-Iranian Supreme Committee.</div>'

r_str = r'<div style="background-color: yellow; display: inline;" id="([a-zA-Z0-9]{12})" data-annotation="(((?!<div)(?!</div>).)*)</div>'


### test for generating end2end_EL input data


# s = 'Anarchism is a <a href="political philosophy">political philosophy</a> that advocates <a href="stateless society">stateless societies</a> often defined as <a href="self-governance">self-governed</a> voluntary institutions, but that several authors have defined as more specific institutions based on non-<a href="Hierarchy">hierarchical</a> <a href="Free association (communism and anarchism)">free associations</a>. Anarchism holds the <a href="state (polity)">state</a> to be undesirable, unnecessary, or harmful. While anti-statism is central, some argue that anarchism entails opposing <a href="authority">authority</a> or <a href="hierarchical organization">hierarchical organization</a> in the conduct of human relations, including, but not limited to, the state system.'
# s_str = r'<a href="(.*?)">(.*?)</a>'
#
# for i in re.finditer(s_str, s):
#     print(s[i.start():i.end()])


s = 'Anarchism is a <a href=" "> <a href="political philosophy">political philosophy</a>'
# s_str = r'<a href="(((?!(<a))(?!(a>)).)+)">(((?!(<a))(?!(a>)).)+)</a>'
s_str = r'<a href="(((?!<a)(?!a>).)+)">(((?!<a)(?!a>).)+)</a>'

for i in re.finditer(s_str, s):
    print(s[i.start():i.end()])


# a new example where regular expression doesn't contain specific word

# find the substring which starts with 'a', ends with 'n', doesn't have 'cde'


# s = 'abcdefnahcdklmn'
# # r_s = '(a((?!(cde)).)+n)'
# r_s = '(a((?!bcd)(?!dkl).)+n)'
# for i in re.finditer(r_s, s):
#     print(i.start(), i.end(), s[i.start(): i.end()])

