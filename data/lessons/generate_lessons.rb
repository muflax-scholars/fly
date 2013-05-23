#!/usr/bin/env ruby
# -*- encoding: utf-8 -*-
# Copyright muflax <mail@muflax.com>, 2013
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>

# Generates lessons for the pseudosteno track. Pseudo is introduced in 5 steps:
#
# 1. Single keys where the pseudo character is identical to the steno character.
# 2. Pseudo characters that have the shape of a row, i.e. multiple consecutive fingers on the same level.
# 3. Pseudo characters on a row, i.e. produced by pressing two keys with one finger.
# 4. Pseudo characters on rows with gaps.
# 5. Pseudo characters on blocks, i.e. rows on both levels.
# 6. All remaining pseudo characters.
#
# This covers all of pseudo, but not all possible key combinations. Those are introduced manually via the Phoenix Theory track.

# for reference
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

# stroke -> pseudo
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
               "A-"    => "A",
               "AEU"   => "[AY]",
               "AO"    => "[OO]",    # only for one-stroke words spelt with "oo"; otherwise it's AOU
               "AOE"   => "[EE]",
               "AOEU"  => "[EYE]",
               "AOU"   => "[OOH]",
               "AU"    => "[AW]",
               "-E"    => "E",
               "EU"    => "I",
               "H-"    => "H",
               "HR-"   => "L",
               "K-"    => "K",
               "KH"    => "[CH]-",   # new
               "KP-"   => "X",
               "KPW"   => "[KN]-",   # new
               "KR-"   => "C",
               "KW"    => "Q",
               "KWR"   => "Y",
               "O-"    => "O",
               "OE"    => "[OH]",
               "OU"    => "[OW]",
               "P-"    => "P",
               "PH"    => "M",
               "PW"    => "B",
               "R-"    => "R",
               "S-"    => "S",
               "SKWR"  => "J",
               "SR"    => "V",
               "SWR"   => "Z-",      # new
               "T-"    => "T",
               "TK"    => "D",
               "TKPW"  => "G",
               "TP-"   => "F",
               "TPH"   => "N",
               "-U"    => "U",
               "W-"    => "W",
               "*"     => "*",       # not technically pseudo, but only exception we need
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

ordering = {
            :single => [
                        "S-", #
                        "A-",
                        "-R", #
                        "K-",
                        "-L",
                        "T-", #
                        "-E",
                        "P-", #
                        "-G",
                        "O-",
                        "W-",
                        "-T", #
                        "-U",
                        "*",
                        "-S", #
                        "H-", 
                        "-F",
                        "R-", #
                        "-D",
                        "-P", #
                        "-B",
                        "-Z",
                       ],

            :rows => [
                      "-BG",
                      "-BGS",
                      "-FP",
                      "-FPL",
                      "-GS",
                      "-PL",
                      "-SZ",
                      "AEU",
                      "AO",
                      "AOE",
                      "AOEU",
                      "EU",
                      "KW",
                      "KWR",
                      "OE",
                      "PH",
                      "SKWR",
                      "TP-",
                      "TPH",
                     ],

            :cols => [
                      "-PB",
                      "HR-",
                      "PW",
                      "TK",
                     ],

            :gaps => [
                      "-GZ",
                      "AOU",
                      "AU",
                      "KR-",
                      "OU",
                      "SR",
                      "SWR",
                     ],

            :blocks => [
                        "-PBLG",
                        "TKPW",
                       ],

            :rest => [
                      "*S",
                      "-FB",
                      "-GT",
                      "KH",
                      "KP-",
                      "KPW",
                     ]
           }

review = []
ordering.each.with_index(1) do |(name, chars), i|
  make_lesson "#{i}_#{name}", :spaced, Hash[chars.map{|c| [PseudoSteno[c], c]}]
  review += chars
  make_lesson "#{i}_#{name}_review", :randomized, Hash[review.map{|c| [PseudoSteno[c], c]}]
end

# make sure the specs are valid
review.each do |char|
  puts "#{char} missing in PseudoSteno..." unless PseudoSteno.include? char
end
