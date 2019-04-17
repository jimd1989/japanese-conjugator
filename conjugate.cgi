#!/usr/bin/ruby
# JUN 2017
# encoding=utf-8
require 'set'
require 'uri'
require 'cgi'
$F = false
$T = true

#data
cgi = CGI.new
puts cgi.header
$IE = Set.new ['み', 'め', 'い', 'き', 'ち', 'し', 'に', 'ひ', 'り', 'ゐ', 'え', 'け', 'せ', 'て', 'ね', 'へ', 'れ', 'ゑ', 'べ', 'び', 'ぴ', 'ぺ']
$IRREGULAR = Set.new ['脂ぎる', 'ビビる', '契る', '散る', 'どじる', '愚痴る', '入る', '走る', '穿る', '迸る', 'いびる', '弄る', '煎る', '要る', '限る', '齧る', '切る', '軋る',
		      '抉る', '参る', '混じる', '滅入る', '見縊る', '漲る', '捥る', '文字る', '毟る', '挘る', '詰る', '捩る', '握る', '躙る', '罵る', '陥る', 'せびる', '知る',
		      '謗る', '滾る', '魂消る', 'とちる', '野次る', '過ぎる', '横切る', '焦る', '嘲る', '駄弁る', '彫る', '選る', '耽る', '臥せる', '侍る', '減る', '捻る',
		      '翻る', '火照る', '返る', '孵る', '陰る', '翔る', '蹴る', 'くねる', '覆る', '舐める', '嘗める', '甞める', '練る', 'のめる', '滑る', '阿る', '競る', '挵る',
		      '喋る', '茂る', '湿気る', '哮る', '猛る', '照る', '抓る', '畝る', '蘇る'] 
$ROOT = {'う' => 'い', 'く' => 'き', 'す' => 'し', 'つ' => 'ち', 'む' => 'み', 'る' => 'り', 'ぬ' => 'に', 'ぶ' => 'び'}
$CAUSATIVE = {'う' => 'わせる', 'く' => 'かせる', 'す' => 'させる', 'つ' => 'たせる', 'む' => 'ませる', 'る' => 'らせる', 'ぐ' => 'がせる', 'ぬ' => 'なせる', 'ぶ' => 'ばせる'}
$PASSIVE = {'う' => 'われる', 'く' => 'かれる', 'す' => 'される', 'つ' => 'たれる', 'む' => 'まれる', 'る' => 'られる', 'ぐ' => 'がれる', 'ぬ' => 'なれる', 'ぶ' => 'ばれる'}
$POTENTIAL = {'う' => 'える', 'く' => 'ける', 'す' => 'せる', 'つ' => 'てる', 'む' => 'める', 'る' => 'れる', 'ぐ' => 'げる', 'ぬ' => 'ねる', 'ぶ' => 'べる'}
$NAI = {'う' => 'わない', 'く' => 'かない', 'す' => 'さない', 'つ' => 'たない', 'む' => 'まない', 'る' => 'らない', 'ぐ' => 'がない', 'ぬ' => 'なない', 'ぶ' => 'ばない'}
$TE = {'う' => 'って', 'く' => 'いて', 'す' => 'して', 'つ' => 'って', 'む' => 'んで', 'る' => 'って', 'い' => 'くて', 'ぐ' => 'いで', 'ぬ' => 'んで', 'ぶ' => 'んで', 'ん' => 'んで'}
$TA = {'う' => 'った', 'く' => 'いた', 'す' => 'した', 'つ' => 'った', 'む' => 'んだ', 'る' => 'った', 'い' => 'かった', 'ぐ' => 'いだ', 'ぬ' => 'んだ', 'ぶ' => 'んだ', 'ん' => 'んでした'}
$VOLITIONAL = {'う' => 'おう', 'く' => 'こう', 'す' => 'そう', 'つ' => 'とう', 'む' => 'もう', 'る' => 'ろう', 'ぐ' => 'ごう', 'ぬ' => 'のう', 'ぶ' => 'ぼう'}

# initialization
def godan?(kanji, reading, rlast)
	if rlast == 'る'
		nextchar = reading[reading.length - 2]
		if $IE.include?(nextchar)
			if $IRREGULAR.include?(kanji)
				$T
			else
				$F
			end
		else
			$T
		end
	else
		$T
	end
end

Struct.new("Verb", :kanji, :read, :last, :godan, :masu)
kanji = CGI.unescapeHTML(URI.unescape(cgi['kanji']))
reading = CGI.unescapeHTML(URI.unescape(cgi['reading']))
last = reading[-1]
C = Struct::Verb.new(kanji, reading, last, godan?(kanji, reading, last), $F)

class String
	def just
		self[0 .. -2]
	end
end

#conjugation functions
def ch(v, new_reading, godan, masu)
	Struct::Verb.new(v.kanji, new_reading, new_reading[-1], godan, masu)
end

$CON = {'root' => lambda{|v| v.godan ? ch(v, v.read.just + $ROOT[v.last], $T, $F) : ch(v, v.read.just, $F, $F)},
	'caus' => lambda{|v| v.godan ? ch(v, v.read.just + $CAUSATIVE[v.last], $F, $F) : ch(v, v.read.just + 'させる', $F, $F)},
	'pass' => lambda{|v| v.godan ? ch(v, v.read.just + $PASSIVE[v.last], $F, $F) : ch(v, v.read.just + 'られる', $F, $F)},
	'pot'  => lambda{|v| v.godan ? ch(v, v.read.just + $POTENTIAL[v.last], $F, $F) : ch(v, v.read.just + 'られる', $F, $F)},
	'masu' => lambda{|v| nv = $CON['root'].call(v) ; ch(nv, nv.read + 'ます', $T, $T)},
	'nai'  => lambda{|v| v.masu ? ch(v, v.read.just + 'せん', $T, $T) : v.godan ? ch(v, v.read.just + $NAI[v.last], $T, $F) : ch(v, v.read.just + 'ない', $T, $F)},
	'te'   => lambda{|v| v.godan ? ch(v, v.read.just + $TE[v.last], $F, $F) : ch(v, v.read.just + 'て', $F, $F)},
	'ta'   => lambda{|v| v.godan ? ch(v, v.read.just + $TA[v.last], $F, $F) : ch(v, v.read.just + 'た', $F, $F)},
	'vol'  => lambda{|v| v.masu ? ch(v, v.read.just + 'しょう', $F, $F) : v.godan ? ch(v, v.read.just + $VOLITIONAL[v.last], $F, $F) : ch(v, v.read.just + 'よう', $F, $F)}}

def conjugate(v, cs)
	new_reading = cs.inject(v) {|acc, x| x == '' ? acc : $CON[x].call(acc)}.read
	puts '<h1>' + v.kanji.just + new_reading[v.read.length - 1 .. new_reading.length] + '</h1>'
end

# main {2 root, 3 caus, 4 pass, 5 pot, 6 masu, 7 nai, 8 te, 9 ta, 10 vol}
puts '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"></head><body>'
case
        when cgi['root'] != ''
                conjugate(C, [cgi['root'], '', '', '', '', '', '', '', ''])
        when cgi['vol'] != ''
                conjugate(C, ['', '', '', '', cgi['masu'], '', '', '', cgi['vol']])
        when cgi['te'] != ''
                conjugate(C, ['', cgi['caus'], cgi['pass'], cgi['pot'], cgi['masu'], cgi['nai'], cgi['te'], '', ''])
        else
                conjugate(C, ['', cgi['caus'], cgi['pass'], cgi['pot'], cgi['masu'], cgi['nai'], '', cgi['ta'], ''])
end
puts '</body></html>'
