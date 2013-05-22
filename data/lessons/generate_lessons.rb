#!/usr/bin/env ruby
# -*- encoding: utf-8 -*-
# Copyright muflax <mail@muflax.com>, 2013
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>

# Generates lessons for the pseudosteno track.

StenoKeys = [
             # left hand
             ["",    "S-",  ""],    # L4
             ["T-",  "K-",  "T+K"], # L3
             ["P-",  "W-",  "P+W"], # L2
             ["H-",  "R-",  "H+R"], # L1
             ["*",   "*",   ""],    # L1

             # thumbs
             ["A+O", "A-",  "O-"],  # LT
             ["-E",  "-U",  "E+U"], # RT

             # right hand
             ["*",   "*",   ""],    # R1
             ["-F",  "-R",  "F+R"], # R1
             ["-P",  "-B",  "P+B"], # R2
             ["-L",  "-G",  "L+G"], # R3
             ["-T",  "-S",  "T+S"], # R4
             ["-D",  "-Z",  "D+Z"], # R4
             ["T+D", "S+Z", ""],    # R4
            ]

PseudoSteno = { 
               "*S"    => "-[ST]",   # new
               "-B"    => "-B",
               "-BG"   => "-K",
               "-BGS"  => "-X",
               "-D"    => "-D",      # also -ed
               "-F"    => "-F",
               "-FB"   => "-V",      # new
               "-FP"   => "-[CH]",   # new
               "-FPL"  => "-[MP",    # new
               "-G"    => "-G",      # also -ing
               "-GS"   => "-[SH]",   # new
               "-GT"   => "-[TH]",   # new
               "-GZ"   => "-[SHUN]", # or -ings
               "-L"    => "-L",
               "-P"    => "-P",
               "-PB"   => "-N",
               "-PBLG" => "-J",
               "-PL"   => "-M",
               "-R"    => "-R",
               "-S"    => "-S",
               "-SZ"   => "-[SS]",   # new
               "-T"    => "-T",
               "-V"    => "-V",
               "-Z"    => "-Z",
               "A"     => "A",
               "AEU"   => "[AY]",
               "AO"    => "[OO]",    # only for one-stroke words spelt with "oo"; otherwise it's AOU
               "AOE"   => "[EE]",
               "AOEU"  => "[EYE]",
               "AOU"   => "[OOH]",
               "AU"    => "[AW]",
               "E"     => "E",
               "EU"    => "I",
               "H"     => "H",
               "HR"    => "L",
               "K"     => "K",
               "KH"    => "[CH]-",   # new
               "KP"    => "X",
               "KPW"   => "[KN]-",   # new
               "KR"    => "C",
               "KW"    => "Q",
               "KWR"   => "Y",
               "O"     => "O",
               "OE"    => "[OH]",
               "OU"    => "[OW]",
               "P"     => "P",
               "PH"    => "M",
               "PW"    => "B",
               "R"     => "R",
               "S"     => "S",
               "SKWR"  => "J",
               "SR"    => "V",
               "SWR"   => "Z-",      # new
               "T"     => "T",
               "TK"    => "D",
               "TKPW"  => "G",
               "TP"    => "F",
               "TPH"   => "N",
               "U"     => "U",
               "W"     => "W",
              }

def make_lesson name, type=:spaced, words={}
  File.open("#{name}.les", "w") do |les|
    File.open("#{name}.chd", "w") do |chd|
      # header
      les.puts "<#{type}, word>"
      chd.puts # empty line

      # word / chord pair
      words.each do |word, translation|
        les.puts word
        chd.puts translation
      end
    end
  end
end

# order in which steno keys are introduced
steno = [
         "S-",
         "T-",
         "K-",
         "TK",
         "P-",
         "W-",
         "PW",
         "H-",
         "R-",
         "HR-",
         "*",
         "AO",
         "A-",
         "O-",
         "-E",
         "-U",
         "EU",
         "-F",
         "-R",
         "FR",
         "-P",
         "-B",
         "-PB",
         "-L",
         "-G",
         "LG",
         "-T",
         "-S",
         "-TS",
         "-D",
         "-Z",
         "DZ",
         "TD",
         "SZ",
        ]

# order in which pseudosteno is introduced
pseudo = [
          "*S",
          "-B",
          "-BG",
          "-BGS",
          "-D",
          "-F",
          "-FB",
          "-FP",
          "-FPL",
          "-G",
          "-GS",
          "-GT",
          "-GZ",
          "-L",
          "-P",
          "-PB",
          "-PBLG",
          "-PL",
          "-R",
          "-S",
          "-SZ",
          "-T",
          "-V",
          "-Z",
          "A",
          "AEU",
          "AO",
          "AOE",
          "AOEU",
          "AOU",
          "AU",
          "E",
          "EU",
          "H",
          "HR",
          "K",
          "KH",
          "KP",
          "KPW",
          "KR",
          "KW",
          "KWR",
          "O",
          "OE",
          "OU",
          "P",
          "PH",
          "PW",
          "R",
          "S",
          "SKWR",
          "SR",
          "SWR",
          "T",
          "TK",
          "TKPW",
          "TP",
          "TPH",
          "U",
          "W",
         ]

make_lesson "1_single_key",          :spaced,     Hash[steno.zip(steno)]
make_lesson "1_single_key_review",   :randomized, Hash[steno.zip(steno)]
make_lesson "2_multi_key",           :spaced,     {}
make_lesson "2_multi_key_review",    :randomized, {}
make_lesson "3_pseudo",              :spaced,     Hash[pseudo.map{|p| [PseudoSteno[p], p]}]
make_lesson "3_pseudo_review",       :randomized, Hash[pseudo.map{|p| [PseudoSteno[p], p]}]
make_lesson "4_multi_pseudo",        :spaced,     {}
make_lesson "4_multi_pseudo_review", :randomized, {}


# make_lesson "test", :spaced, PseudoSteno.invert
