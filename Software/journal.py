#!/usr/bin/env python3
"""
writerdeck journal — a daily writing practice tool.
Entries are write-once and saved as plain text.

Usage:
    python3 journal.py
"""

import curses
import os
import random
import sys
import textwrap
import time
from datetime import datetime, timedelta

# ── Config ──────────────────────────────────────────────────────────────────

JOURNAL_DIR = os.path.expanduser("~/journal")
FILE_EXT = ".txt"
TAB_WIDTH = 4

# ── Writing Prompts ─────────────────────────────────────────────────────────

PROMPTS = [
    "What happened today?",
    "What was the best thing that happened today?",
    "What was the worst thing that happened today?",
    "What was the most interesting thing I saw or heard today?",
    "What was the most challenging thing I faced today?",
    "What am I grateful for today?",
    "What did I learn today?",
    "What was the most fun thing I did today?",
    "What was the most surprising thing that happened today?",
    "What did I do today that I am proud of?",
    "What are my goals and objectives related to this problem or challenge?",
    "What are some potential solutions to this problem or challenge?",
    "What are some creative and unconventional solutions I can consider?",
    "What are some pros and cons of each potential solution?",
    "How can I collaborate with others to find a solution?",
    "What are some resources I can utilize to help solve this problem or challenge?",
    "How can I apply my skills, knowledge, and experience to this problem or challenge?",
    "What are some potential roadblocks or challenges to implementing a solution, and how can I overcome them?",
    "How can I prioritize and organize my thoughts and ideas to effectively solve this problem or challenge?",
    "What beliefs or messages about my body do I need to let go of in order to cultivate more self-love and acceptance?",
    "What activities or practices help me feel connected to and in tune with my body?",
    "How can I be more compassionate towards my body, especially when I’m feeling self-critical or negative?",
    "What role does social media or the media in general play in shaping my body image, and how can I cultivate a more positive relationship with these sources of influence?",
    "What would it feel like to let go of the need to compare my body to others, and instead focus on my own unique strengths and beauty?",
    "What are some ways I can prioritize my physical health and well-being, without falling into the trap of diet culture or body shaming?",
    "How can I shift my focus from appearance-based goals (e.g. weight loss, achieving a certain body shape) to more holistic measures of health and wellness (e.g. energy levels, mood, strength, etc.)?",
    "What does it mean to truly embody self-love and body positivity, and how can I take small steps towards this every day?",
    "How can I cultivate a sense of appreciation and love for my body, even if it doesn’t conform to societal ideals?",
    "What are some ways I can celebrate and care for my body, regardless of its shape or size?",
    "How do I get to use my creativity on a daily basis?",
    "What is one thing that I have always wanted to create, and what steps can I take to make it a reality?",
    "What is one place or environment that inspires my creativity, and how can I create more opportunities to be in that space?",
    "What are my passions and interests, and how can I incorporate them into my work or personal life?",
    "What is one small creative project that I can do today, and how can I make it unique to my personal style?",
    "What is one fear or obstacle that is holding me back creatively, and what can I do to overcome it?",
    "What is one thing that I can learn or experiment with in order to expand my creative skills and knowledge?",
    "What is one challenge or prompt that I can give myself to push myself creatively?",
    "What is one way I can creatively express gratitude, love, or appreciation for someone in my life?",
    "How can I challenge myself to think outside of the box and embrace new and creative ideas?",
    "How can I surround myself with people and environments that foster creativity and inspiration?",
    "What are some ways I can take time for myself and recharge my batteries to cultivate creativity and inspiration?",
    "What are some hobbies or activities I can pursue to tap into my creativity and imagination?",
    "How can I incorporate more play and fun into my life to foster creativity and inspiration?",
    "What are some ways I can break out of my comfort zone and try new things to stimulate creativity and inspiration?",
    "How can I be more open-minded and receptive to new ideas and perspectives?",
    "What are some ways I can use technology and innovation to enhance my creativity and inspiration?",
    "How can I seek out new experiences and adventures to expand my horizons and inspire my creativity?",
    "How can I create a supportive and nurturing environment for my mind, body, and soul to encourage creativity and inspiration?",
    "Write a story from the perspective of an inanimate object that has come to life.",
    "Write a poem about a childhood memory that has stayed with you.",
    "Write about a character who wakes up one day with a superpower.",
    "Write a poem about the changing of the seasons and the beauty of nature.",
    "Write a story that begins with the sentence “The door creaked open, revealing a long-forgotten room.”",
    "Write a story about a group of people who are stranded on a deserted island.",
    "Write a poem that explores the concept of time and how it shapes our lives.",
    "Write a story from the perspective of a character who has lost their memory and is trying to piece together their past.",
    "Write a poem that reflects on the beauty of everyday moments.",
    "Write a story about a time traveler who accidentally gets stuck in the wrong time period.",
    "Write about a relationship that taught you an important lesson about yourself or the world around you.",
    "Write a story about a character who discovers a mysterious book with a hidden message.",
    "Write a poem that uses the theme of water to convey a deeper meaning or emotion.",
    "Write about a place that has had a significant impact on your life, and what memories or emotions it brings up for you.",
    "Write a story about a character who is forced to confront their deepest fear.",
    "Write a poem that explores the idea of home and what it means to you.",
    "Write a story from the perspective of an animal who is trying to survive in the wilderness.",
    "Write about an experience that taught you a valuable lesson about forgiveness or acceptance.",
    "Write a story about a character who receives a letter from a long-lost relative with a surprising revelation.",
    "How does my body feel today?",
    "What am I nervous or anxious about today?",
    "What actions can I take on each of the things that make me nervous or anxious?",
    "What are my top priorities for the day?",
    "What’s something I can do to make today amazing?",
    "What did I learn today? How can I apply this knowledge in the future?",
    "What challenges did I face today? How did I overcome them? What can I learn from these experiences?",
    "What did I do today that brought me joy or fulfillment? How can I incorporate more of these activities into my daily routine?",
    "What was a moment of joy, delight, or contentment today?",
    "What was a small detail I noticed today?",
    "What was the weather like today?",
    "What am I thankful for today?",
    "What could I have done differently today?",
    "How can I make tomorrow even better?",
    "What is the decision I need to make?",
    "When do I need to make this decision?",
    "What is the desired outcome I hope to achieve?",
    "What are the pros and cons of each option?",
    "What are my fears or concerns about making this decision?",
    "What insights or lessons have I gained from similar decisions I’ve made in the past?",
    "How do these lessons or insights apply to this situation?",
    "What advice would I give to a friend in this same situation?",
    "What is my instinct or intuition telling me about this decision?",
    "What impact will this decision have on myself and others?",
    "How does this decision align with my values?",
    "What resources or support do I need to make this decision with confidence and clarity?",
    "What is the worst-case scenario if I make this decision?",
    "What facts do I have to support my decision?",
    "How do I feel about my decision?",
    "How confident am I feeling about this decision?",
    "What are my next steps for this decision?",
    "What was the most memorable dream I had last night? Write down as many details as you can remember.",
    "What recurring themes or symbols appear in my dreams? Are there any patterns I can identify?",
    "What emotions did I feel in my dream, and do they relate to any current issues in my waking life?",
    "What do I think my dream is trying to tell me? How can I apply its message to my life?",
    "If I could have any dream I wanted tonight, what would it be about?",
    "If I could ask a dream character any question, who would I choose, and what would I ask them?",
    "What are some of the most bizarre or surreal dreams I’ve ever had? What do I think they mean?",
    "What is the most common type of dream I have (like nightmares, flying dreams, etc.)? What do I think it says about my psyche?",
    "What are three things that went well today, and why?",
    "What were the highlights of my day?",
    "What are three things that I could have done differently today, and how can I learn from these experiences?",
    "What did I learn today?",
    "How did I show gratitude today?",
    "What were some challenges I faced today and how did I overcome them?",
    "What did I do to take care of myself today?",
    "What did I do to help others today?",
    "How did I prioritize my time today?",
    "What did I do to bring positivity into my day?",
    "What did I do today that made me proud of myself?",
    "What were the most important events of the day?",
    "How did I feel at different moments throughout the day?",
    "What were some unexpected events that took place today?",
    "Who did I interact with today and what were those interactions like?",
    "What did I accomplish today?",
    "What are some things I would like to do differently tomorrow?",
    "What did I do to relax and recharge today?",
    "What were some of the sights, sounds, and smells I experienced today?",
    "How did I handle any difficult situations that arose today?",
    "What are some things I am looking forward to tomorrow?",
    "What emotions did I experience today?",
    "How did I respond to each emotion? What triggered each emotion?",
    "What did I do to make a positive impact on someone else’s day?",
    "What am I looking forward to tomorrow?",
    "What can I do to prepare for a peaceful night’s sleep?",
    "What was the most significant event of my day and why was it important?",
    "How did I handle any conflicts or difficult situations today?",
    "What did I learn about myself today?",
    "What are some things I can do differently tomorrow to have an even better day?",
    "Who made a positive impact on my day and how?",
    "What did I do to make someone else’s day better?",
    "What are some things I want to remember about today?",
    "What is something silly that always makes me laugh?",
    "What is a favorite childhood memory that still brings me joy?",
    "If I could live in any time period or place, where would I choose and why?",
    "What is my favorite meal or type of food, and why do I love it so much?",
    "If I could have any superpower, what would it be and why?",
    "What is a book or movie that always puts me in a good mood, and why?",
    "What is something I’ve always wanted to try but haven’t yet? How might I make that happen?",
    "What is one thing I can’t live without?",
    "What is one funny story about my life that I don’t mind sharing with other people?",
    "What is something about myself that I know is quirky?",
    "If I could be any fictional character, who would I choose and why?",
    "What is the most outrageous outfit or costume I’ve ever worn? Where did I wear it, and how did I feel?",
    "What is my favorite silly joke or pun, and why does it make me laugh?",
    "What is the best gift I have ever given, and why was it so special?",
    "If I were a superhero, what would be my name, powers, and costume?",
    "What is the funniest prank I have ever played on someone, or that someone has played on me?",
    "If I could magically switch lives with anyone for a day, who would it be and why?",
    "What is my favorite childhood toy or game, and why did I love it so much?",
    "What is my favorite dance move, and can I teach it to someone else (or describe it in words)?",
    "If I could travel anywhere in the world (or beyond), where would I go and what would I do there?",
    "What are my top three goals for the next year?",
    "What are some actionable steps I can take to achieve my goals?",
    "What is one new habit I would like to develop in the next month?",
    "How can I create a plan to make this new habit a consistent part of my routine?",
    "What are three skills or areas of knowledge I would like to develop in the next year?",
    "What resources or support can I seek out to help me achieve my goals?",
    "What are three things that are holding me back from achieving my goals?",
    "How can I work to overcome these obstacles?",
    "What are three small, measurable goals I can set for myself this week?",
    "How will I hold myself accountable for following through on my goals?",
    "What are my long-term career goals? What are some concrete steps I can take to move closer to achieving them?",
    "What are my personal values and how do they relate to my goals?",
    "How can I ensure that my goals are aligned with my values?",
    "What are some potential roadblocks or challenges that I may encounter as I work towards my goals?",
    "How can I develop a plan to overcome roadblocks or challenges to my goals?",
    "How can I track my progress towards my goals?",
    "What tools or systems can I use to stay motivated and on track?",
    "What are three small, specific goals I can set for myself each day?",
    "How can I ensure that my daily actions align with my larger goals and priorities?",
    "What habits do I need in order to achieve my goals?",
    "Who are three people in my life that I am grateful for, and why?",
    "What are three small things that happened today that I am grateful for?",
    "What is one thing that I often take for granted in my life, and how can I cultivate more appreciation and gratitude for it?",
    "What are some positive qualities or strengths that I possess, and how can I be grateful for them?",
    "What is something in my life that I feel “lucky” to have?",
    "What is a simple delight I have been enjoying lately?",
    "What is something I am grateful to have learned recently?",
    "In what ways have I grown as a person over the last year?",
    "What do I like about where I live right now?",
    "What were some moments of joy today?",
    "How does expressing gratitude make me feel right now?",
    "How can I show my gratitude today?",
    "What are some ways I can express gratitude and appreciate the beauty and wonder of the world around me?",
    "What are some areas of my life where I tend to have a fixed mindset?",
    "How can I shift my thinking to adopt a growth mindset instead?",
    "What are some goals that I’ve been afraid to pursue due to fear of failure or rejection?",
    "How can I reframe my mindset to view failure as a natural part of the learning process, and use it as an opportunity for growth?",
    "What are some of my limiting beliefs and self-talk that may be holding me back?",
    "How can I challenge and overcome them?",
    "How can I embrace challenges and failures as opportunities for growth and development, rather than viewing them as setbacks?",
    "How can I cultivate a positive and optimistic attitude, even in the face of adversity and difficulty?",
    "What are some ways I can seek out feedback and constructive criticism to continue growing and improving?",
    "How can I strive for progress, rather than perfection, in my personal and professional life?",
    "What are some of my strengths and areas for growth, and how can I use this knowledge to drive personal development and growth?",
    "How can I seek out new experiences, opportunities, and relationships to broaden my horizons and support personal growth?",
    "How can I foster resilience and perseverance in the face of obstacles and challenges to continue growing and developing?",
    "How can I take responsibility for my thoughts, feelings, and actions, and use them as opportunities for growth and development?",
    "How can I view mistakes and failures as learning opportunities, rather than setbacks or obstacles?",
    "What are some new skills or knowledge areas that I want to develop?",
    "How can I cultivate a curious and open-minded attitude, and seek out new information and knowledge to support growth and development?",
    "What are some ways I can adopt a proactive, rather than reactive, approach to challenges and difficulties?",
    "What memories do I have from my childhood? Are there any happy memories that stand out?",
    "What was my favorite activity as a child? Did I have any hobbies or interests that I loved?",
    "How did I spend my free time as a child? What games did I play? What books did I read?",
    "What did I enjoy most about school? Did I have a favorite subject or teacher?",
    "Did I have any dreams or aspirations as a child? What did I want to be when I grew up?",
    "What were some of the challenges or struggles I faced as a child? How did those experiences shape me?",
    "How did my family and upbringing impact my childhood experiences? What positive or negative influences did I have?",
    "What beliefs or attitudes did I develop as a child that may still be impacting me today?",
    "How can I nurture and care for my inner child now? What activities or experiences bring me joy and playfulness?",
    "What can I learn from my inner child? How can I tap into the curiosity, creativity, and resilience that I had as a child?",
    "What activities or experiences brought me joy as a child?",
    "How can I incorporate these activities into my life now?",
    "How can I nurture my inner child and cultivate a sense of playfulness and wonder?",
    "When was the last time I felt inspired?",
    "Where do I usually find inspiration?",
    "What things inspire me?",
    "Who is someone that inspires me, and what qualities do they possess that I admire?",
    "What is one book or movie that has inspired me, and why?",
    "What are some of my favorite forms of art, literature, or media, and how can they inspire me?",
    "What is one quote or saying that inspires me, and how can I apply its wisdom to my life?",
    "What is one creative project that I have been wanting to work on, and what steps can I take to get started?",
    "When was the last time I felt completely in awe of something, and what was it that inspired that feeling?",
    "What is one thing that I have always wanted to learn, and how can I make time to pursue this interest?",
    "What is one small thing that I can do each day to cultivate a greater sense of inspiration and creativity in my life?",
    "What do I want to focus on this month/week/day?",
    "What are my intentions for the day?",
    "What is my biggest “why” (the deeper purpose or motivation behind my intentions)?",
    "How can I use my “why” to stay focused and committed?",
    "How can I prioritize my time and energy accordingly?",
    "What are some external factors that could impact my ability to focus on my intentions, and how can I plan ahead to address them?",
    "What are some distractions or time-wasters that I need to eliminate in order to focus on what’s truly important?",
    "What brings me the most joy and fulfillment, and how can I make time for those things in my life?",
    "What does happiness mean to me? What can I do to cultivate more happiness and contentment in my life?",
    "What decisions am I facing right now?",
    "How do I define success? What steps can I take to achieve it?",
    "What are my fears and insecurities? How can I work through them to become more confident and self-assured?",
    "What are the most important relationships in my life? How can I strengthen them?",
    "In general, how do I feel about how my life is going right now?",
    "What are some areas of my life where I am currently stuck or feeling stagnant? What steps can I take to move forward and make progress in those areas?",
    "What themes, patterns, or symbols have I noticed in my life lately?",
    "What are some beliefs or assumptions that I hold about myself or the world around me?",
    "When I am faced with challenges or obstacles, what is my usual response?",
    "What are some activities or habits that drain my energy or motivation?",
    "How do I usually handle my emotions and feelings? Are there any emotions that I tend to avoid or suppress?",
    "What are some of the things that I am most grateful for in my life? How can I cultivate more gratitude and appreciation?",
    "What are my fondest memories of the person I have lost?",
    "What are the things I wish I could have said or done with the person before they passed away?",
    "What is the hardest thing about dealing with the loss?",
    "How can I find ways to cope with my grief?",
    "How has this loss impacted my daily routine?",
    "What are the things I have learned about myself or about life in general as a result of this loss?",
    "What are some positive steps I can take to honor the memory of the person I have lost?",
    "How can I find support and comfort during this difficult time?",
    "Who are the people in my life who I can turn to for care and support as I navigate through my grief?",
    "What are some healthy ways I can process my grief, such as through exercise, meditation, or creative outlets like art or music?",
    "What’s going on that makes this time so difficult?",
    "What is causing my distress?",
    "Who can I turn to for support?",
    "How have I coped with difficult times in the past?",
    "What are some things I am thankful for, even in challenging circumstances?",
    "How can I cultivate a sense of appreciation and optimism in the face of adversity?",
    "What self-care practices have helped me in the past?",
    "What can I learn from this experience? What lessons might I learn?",
    "How can I reframe the situation?",
    "What actions can I take to improve the situation?",
    "What positive things do I have in my life right now?",
    "What can I do to take care of myself right now?",
    "What are my personal values and beliefs? How do they shape my identity?",
    "What are some of the roles that I take on in my life? How do these roles contribute to my sense of identity?",
    "How do I define myself in terms of my relationships with others? How do these relationships shape my sense of self?",
    "What do I know about my cultural or ethnic background? How does my cultural or ethnic background shape my identity?",
    "What are some of the strengths, talents, or unique qualities that I possess? How do they contribute to my sense of self?",
    "How does my physical appearance shape my sense of identity?",
    "What life experiences have shaped who I am today?",
    "What are some of the fears or doubts that I have about my identity? How can I address these fears or doubts in a healthy way?",
    "How do I balance my need for individuality with my need for a sense of community or belonging?",
    "What are some of the things that I want to achieve or accomplish in life? How do these goals contribute to my sense of identity?",
    "What is one of my earliest childhood memories?",
    "What emotions does this memory evoke?",
    "What is a happy memory from my childhood? What made it so special?",
    "What is a difficult memory from my past? How has this memory shaped me as a person?",
    "Who were some of my closest friends growing up? What impact did they have on my life?",
    "Who were some of my role models or mentors growing up? What impact did they have on my life?",
    "What were some of my favorite hobbies or activities growing up? Do I still enjoy them today?",
    "What were some of the major milestones or accomplishments I achieved in my life? How did they make me feel?",
    "What were some of the most challenging or transformative experiences I’ve had in my life? How have they shaped my perspective or values?",
    "What were some of the biggest surprises or unexpected turns my life has taken? How have I coped with these changes?",
    "What were some of the people or experiences that have brought me the most joy or meaning in my life? How can I cultivate more of these positive influences in my present?",
    "What are my favorite hobbies or activities?",
    "How do my favorite hobbies or activities make me feel?",
    "If I had all the time and resources I needed, what activities or hobbies would I pursue?",
    "What is it about my favorite hobby that I enjoy the most? How can I incorporate more of that into my life?",
    "Who do I know that shares my passion or hobby, and how can we collaborate or support each other?",
    "What skills do I possess that could be applied to a new hobby or activity?",
    "What is something I have always wanted to try but haven’t yet, and what is holding me back?",
    "If I could turn my passion or hobby into a career or side business, what steps could I take to make it happen?",
    "What am I afraid of?",
    "What is the source of my fear? Where does it come from?",
    "How does my fear affect my life? In what ways does it hold me back?",
    "What would my life be like without this fear? What would I be able to accomplish or experience?",
    "How can I reframe my fear? Is there a way to look at the situation or issue differently?",
    "What steps can I take to face my fear? What action can I take to move through it?",
    "Who can I turn to for support? Who can help me face my fear?",
    "What have I learned from past experiences of facing fear? What worked well, and what didn’t work?",
    "How can I use my fear as motivation? Can I turn my fear into a positive force that drives me forward?",
    "What is the worst that can happen if I face my fear? What is the best that can happen?",
    "What are some fears or limiting beliefs that are holding me back?",
    "How can I work to overcome them?",
    "What resources or support can I seek out to help me overcome my fears?",
    "What emotion am I feeling right now? Write down any emotions that come to mind, no matter how big or small they may seem.",
    "Where do I feel this emotion in my body? What are the physical sensations I experience when I feel this emotion? Does it manifest in a certain part of my body or in a specific way?",
    "What triggered this emotion? Was it a thought, a memory, or something someone said or did?",
    "How am I responding to this emotion?",
    "When was the last time I felt this way?",
    "What emotions do I feel most often?",
    "What emotions do I avoid feeling?",
    "How did my emotions affect my thoughts and behavior today?",
    "How can I express this emotion in a healthy way?",
    "What can I learn from this emotion? Consider how this emotion can teach you something about yourself, your values, or your needs.",
    "What were some moments of stress or frustration today?",
    "What were some moments of peace or calm today?",
    "How did I handle negative emotions today?",
    "How can I better cope with difficult emotions in the future?",
    "What are some ways I can promote positivity and happiness in my life?",
    "How can I support myself through this emotion? Write down self-care strategies that can help you feel more grounded and centered when experiencing this emotion.",
    "What is happening in this present moment?",
    "What are five things I can see right now, and what colors, shapes, and textures do they have?",
    "If my mind was like the ocean right now, what is the water like?",
    "What thoughts am I observing right now?",
    "What sensory information am I getting in this present moment?",
    "What are three things I can hear right now, and how do they sound?",
    "What are three things I can feel physically right now, such as the weight of my body on a chair or the texture of my clothing?",
    "What are three things I can smell right now, and how do they smell?",
    "What are three things I can taste right now, and how do they taste?",
    "What emotions am I feeling right now, and how can I practice acceptance and self-compassion towards them?",
    "What thoughts are running through my mind right now, and how can I acknowledge them without getting caught up in them?",
    "What are three things I am looking forward to in the next hour, and how can I stay present and open to experiencing them fully?",
    "What are three things that are worrying me right now, and how can I practice mindfulness to reduce my stress and anxiety?",
    "What are three small actions I can take right now to bring myself into the present moment, such as taking a deep breath, stretching, or savoring a sip of tea or coffee?",
    "What’s on my mind this morning?",
    "What am I looking forward to today?",
    "What do I need to do today?",
    "What are my goals for today?",
    "What are some ways I can be productive today?",
    "What can I do today to take care of my physical and mental health?",
    "What are some challenges I might face today and how can I prepare for them?",
    "How can I prioritize self-care today?",
    "Who can I reach out to for support today?",
    "What is one thing I can do today to help someone else?",
    "How can I bring positivity into my day today?",
    "What positive affirmations can I tell myself to start my day on a positive note?",
    "What mindset or attitude do I want to cultivate today? How can I remind myself of this throughout the day?",
    "What makes me glad to be alive today?",
    "What am I most grateful for at the beginning of this new year?",
    "What lessons did the previous year teach me?",
    "What are three things I accomplished last year?",
    "What values will guide my choices this year?",
    "What would I like to savor or enjoy more often this year?",
    "What are three goals I hope to accomplish this year?",
    "What new skill would I like to learn or improve this year?",
    "What relationships are most important to me? How can I continue to invest in these relationships this year?",
    "What problems would I like to solve this year?",
    "How would I like to grow or develop as a person this year?",
    "What is one habit I would like to build this year?",
    "What is something I want to do for others in the coming year?",
    "What is something I want to do for myself in the coming year?",
    "How can I prioritize my health and/or fitness this year?",
    "What new experiences do I want to try this year?",
    "What new place would I like to visit this year?",
    "What new creative project or hobby would I like to start this year?",
    "What fear do I want to overcome this year?",
    "How can I show more gratitude this year?",
    "How can I rest or relax more often this year?",
    "What am I looking forward to in the coming year?",
    "What word or phrase would I like to give this year?",
    "What is my biggest dream for the year ahead?",
    "What are three qualities I want to embody in my daily life?",
    "What are my biggest fears and how can I overcome them?",
    "What are some limiting beliefs that hold me back, and how can I challenge them?",
    "What are some habits I want to cultivate or break, and how can I make progress towards those goals?",
    "What are some past mistakes or failures that have taught me valuable lessons, and how can I apply those lessons to my current life?",
    "How can I set and work towards achievable, yet challenging, goals to drive personal growth and development?",
    "How can I be more proactive and intentional about seeking out growth opportunities, rather than waiting for them to come to me?",
    "How can I balance taking risks and stepping outside of my comfort zone with taking care of myself and my well-being?",
    "How can I develop a growth mindset in areas that are difficult for me, such as public speaking or self-promotion?",
    "How can I seek out and embrace constructive criticism and feedback, and use it as an opportunity for growth and development?",
    "How can I cultivate a supportive and encouraging environment for personal growth and development, both within myself and in my relationships with others?",
    "What are some ways I can contribute to my community or the world around me?",
    "How do I communicate my needs and boundaries in my relationships?",
    "What are some ways I can deepen my connections with loved ones?",
    "What are my values and priorities when it comes to relationships?",
    "How do these values influence my actions and choices?",
    "How do I respond to conflict in my relationships?",
    "What communication patterns do I notice when things get difficult?",
    "What are some ways I can show appreciation and gratitude for the people in my life?",
    "How do I express love and affection?",
    "What are some challenges I face in my relationships? How can I work on improving these challenges?",
    "How do I handle disagreements or differences in opinion with my loved ones? What are some healthy ways to approach these situations?",
    "What are my relationship goals?",
    "What do I want to achieve in my current relationships or in future relationships?",
    "What are some areas where I need to work on boundaries in my relationships? How can I create healthier boundaries?",
    "How do I balance my needs with the needs of my partner or loved ones? What are some ways to ensure both parties feel heard and respected?",
    "How do I manage stress and emotions in my relationships?",
    "What are some techniques for managing anxiety or other difficult emotions in relationships?",
    "What is my love language? How do I communicate love and affection to my partner or loved ones?",
    "How do I define self care?",
    "What role does self-care play in my mental, physical, and emotional health?",
    "What are my favorite forms of self care?",
    "What are some ways I can prioritize my physical health and well-being to care for myself?",
    "What forms of exercise do I enjoy?",
    "What activities help me feel calm and centered?",
    "How am I incorporating healthy eating into my daily life?",
    "How am I helping myself get enough sleep?",
    "What are some activities or hobbies that bring me joy and relaxation? How can I make time for these in my life?",
    "How can I better manage and reduce stress and anxiety?",
    "How am I exploring mindfulness practices or meditation?",
    "How do I seek support from others?",
    "How can I prioritize self-care during difficult or challenging times, and avoid neglecting my own needs?",
    "How can I set boundaries with others to make sure I have time and energy for self-care?",
    "How can I seek out and connect with supportive and positive relationships that uplift and empower me?",
    "How can I recognize and address toxic or unhealthy patterns or behaviors, and work towards making positive changes for my well-being?",
    "How can I cultivate self-compassion and self-forgiveness, and avoid self-criticism and negative self-talk?",
    "How can I prioritize self-care when I am feeling overwhelmed or burnt out, and take steps to prevent burnout in the future?",
    "When was the last time I took a break or gave myself some time off? How did it feel?",
    "What are my core values? Take some time to reflect on the values that are most important to you in life, and why they matter to you.",
    "When do I feel most alive? Reflect on the moments, experiences, and activities that make you feel fully present, engaged, and energized.",
    "What gives my life meaning or purpose? Consider the activities, relationships, causes, and values that are most important to you.",
    "What are my strengths and weaknesses? Consider the things you’re good at and the areas where you struggle.",
    "How can I leverage my strengths and work on my weaknesses? Consider ways you can utilize your skills, knowledge, or talent in new ways or find ways for improvement.",
    "What are my goals and aspirations? Write down your short-term and long-term goals, and what steps you need to take to achieve them.",
    "What are my passions and interests? Think about the activities, topics, and causes that inspire and motivate you. How can you incorporate more of these things into your life?",
    "What are my fears and limiting beliefs? Explore the fears and beliefs that may be holding you back from reaching your full potential. How can you challenge and overcome them?",
    "What does my ideal life look like? Envision the life you want to create for yourself, and what steps you need to take to make it a reality.",
    "What have been the most defining moments of my life? Reflect on the experiences that have shaped who you are today, and what you’ve learned from them.",
    "What activities bring me the most joy and fulfillment?",
    "What impact do I hope to make in the world? Reflect on how you can align your daily actions with your deeper sense of purpose.",
    "How have my interests changed over time? Take a trip down memory lane and reflect on the activities that you used to enjoy, as well as the ones that you currently enjoy.",
    "What are some of my most memorable and meaningful experiences? How can they inspire me moving forward?",
    "How can I embrace change and new opportunities in my life?",
    "What are some things that make me feel confident?",
    "How have I overcome challenges in the past, and what did I learn from those experiences?",
    "What is one thing I can do today to step outside of my comfort zone and build my confidence?",
    "What are some negative self-talk patterns that I engage in, and how can I reframe those thoughts in a more positive way?",
    "What are my strengths and how can I utilize them to achieve my goals?",
    "What are some compliments that others have given me in the past, and how can I internalize those positive messages?",
    "How can I take care of myself and practice self-compassion in moments when I feel uncertain or doubtful?",
    "What would I say to a friend who is struggling with self-confidence, and how can I apply that advice to my own life?",
    "How can I embrace my unique qualities and use them to my advantage?",
    "What is one step I can take today to work towards a goal that will build my self-confidence?",
    "What are my unique qualities and strengths, and how can I embrace and celebrate them more fully?",
    "What are three things I accomplished this week that I am proud of?",
    "How can I be kinder to myself today?",
    "What are my unique strengths and how have they helped me in the past?",
    "What is one negative thought I have about myself that I can challenge with a positive thought?",
    "What can I do to take care of myself physically and emotionally today?",
    "What are three things I love about myself?",
    "How have I grown and changed as a person in the past year?",
    "What is a positive affirmation I can repeat to myself throughout the day?",
    "What is one small step I can take today to work towards a personal goal or dream?",
    "What are some values that are important to me, and how do they guide my decisions and actions?",
    "What are some experiences from my past that have shaped who I am today, and how have they influenced my beliefs and attitudes?",
    "What are some things that bring me joy and fulfillment, and how can I incorporate more of them into my life?",
    "What are some patterns of behavior or thought that hold me back, and how can I work to break those patterns?",
    "What are some goals or aspirations I have for my life, and what steps can I take to work towards them?",
    "What are some fears or insecurities that hold me back, and how can I work to overcome them?",
    "What are some relationships that are important to me, and how can I nurture and strengthen those relationships?",
    "What are some mistakes or failures from my past that have taught me valuable lessons, and how can I apply those lessons to my current life?",
    "What are some self-care practices that are important to me, and how can I make them a regular part of my routine?",
    "What are some things that I am grateful for in my life, and how can I cultivate more gratitude on a daily basis?",
    "What triggered negative feelings today?",
    "How do I think others perceive me?",
    "What have others communicated to me about myself?",
    "How do I respond to compliments?",
    "When do I feel valued and loved?",
    "What challenges did I face as a child?",
    "What are my best and worst traits?",
    "What do I need to forgive myself for?",
    "What do I judge others for, and why?",
    "Do I feel guilt or shame for anything?",
    "How do I support others, and do I show myself that same love?",
    "What do I consider to be healthy boundaries?",
    "When do I feel the need to lie, and what is the worst lie I’ve told?",
    "What parts of myself do I hide?",
    "What does spirituality mean to me?",
    "What role does spirituality play in my daily life?",
    "What spiritual books, teachings, or leaders have influenced me? What have I learned from these sources?",
    "How can I integrate my spiritual beliefs and practices into my routines?",
    "How do I define my beliefs and values?",
    "How have my beliefs and values evolved over time?",
    "How do I connect with a higher power or the divine?",
    "What practices or rituals do I find helpful in nurturing my spirituality?",
    "How can I incorporate more spirituality into my daily life?",
    "How can I explore my relationship with the divine or higher power?",
    "What questions or uncertainties do I have about my spirituality? How can I explore these questions and seek answers?",
    "How can I use my spirituality to cultivate a sense of compassion and empathy towards others, and contribute to the greater good of humanity?",
    "What are some of the sources of stress in my life right now?",
    "How have I been coping with stress in the past?",
    "What are some healthy coping mechanisms I can use to manage stress?",
    "How can I prioritize self-care to reduce stress?",
    "What are some positive affirmations I can tell myself to combat stress?",
    "Who can I reach out to for support and encouragement when I am feeling stressed?",
    "How can I reframe negative thoughts and maintain a positive outlook?",
    "What are some activities or hobbies that help me relax and de-stress?",
    "How can I create a stress-free environment at home or at work?",
    "What are some steps I can take to prevent stress from overwhelming me in the future?",
    "What are some practical solutions to the sources of stress in my life?",
    "How can I prioritize my time and responsibilities to reduce stress?",
    "What are some physical activities I can do to relieve stress?",
    "How can I maintain a healthy work-life balance to reduce stress?",
    "How can I stay organized and on track to reduce stress?",
    "How can I find humor and joy in life to combat stress?",
    "What are some self-reflection exercises I can do to reduce stress?",
    "How can I maintain a healthy lifestyle to reduce stress, such as eating well, getting enough sleep, and exercising regularly?",
    "How can I set realistic expectations and boundaries to reduce stress?",
    "What are some things I can do to maintain a positive and relaxed state of mind, such as meditating, practicing mindfulness, or spending time in nature?",
    "Where am I currently traveling to and what are my expectations for this trip?",
    "What are some new things I want to experience and try while on this trip?",
    "What are some things I want to learn or understand better about the culture and people in the places I visit?",
    "How did I feel when I arrived at my destination? What were my first impressions?",
    "What did I do on my first day of travel? What were the highlights?",
    "What are some things I want to do or see while I’m here?",
    "What did I do today? What were the highlights?",
    "What did I learn about the place I’m visiting today?",
    "What are some interesting people I’ve met? What did I learn from them?",
    "What impressions have I gotten from the place I’m visiting?",
    "What’s beautiful or unique about the place I’m visiting?",
    "What was the most memorable moment of my trip so far, and why?",
    "What natural wonders did I see today? How did they make me feel?",
    "Did I engage in any outdoor activities today? What were they, and how did they challenge or inspire me?",
    "What local flora or fauna did I encounter today? What did I learn about them?",
    "Did I take any time to relax today? How did I spend that time?",
    "How am I feeling about my trip so far? What are some things that have surprised me?",
    "What are some new things I want to try before my trip ends?",
    "What have I learned about myself on this trip?",
    "What am I most grateful for on this trip?",
    "What challenges have I faced during my travels, and how have I overcome them?",
    "What are some things I would do differently if I could do this trip over again?",
    "What are some things I will miss most about this place?",
    "Who have I met on this trip that has impacted me, and what did I learn from them?",
    "What are some interesting observations or insights I’ve had about the places I’ve visited?",
    "What have I learned about myself during my travels, and how has this experience changed me?",
    "What are some ways I can take the lessons and experiences from my travels and apply them to my life at home?",
    "What if I had the power to fly? How would I use this ability, and where would I go?",
    "What if I could live anywhere in the world? Where would I choose, and why?",
    "What if I won the lottery? How would my life change, and what would I do with the money?",
    "What if I could switch places with someone for a day? Who would I choose, and what would I do in their shoes?",
    "What if I could meet any famous person, living or dead? Who would I choose, and what would I ask them?",
    "What if I could speak any language fluently? Which language would I choose, and what would I do with this skill?",
    "What if I could relive any day from my past? Which day would I choose, and what would I do differently?",
    "What if I could talk to any animal? Which animal would I choose, and what would I ask them?",
    "What if I had made a different pivotal decision in my past? Which decision would have changed the course of my life?",
]

# ── Journal State ───────────────────────────────────────────────────────────

def ensure_journal_dir():
    os.makedirs(JOURNAL_DIR, exist_ok=True)

def today_str():
    return datetime.now().strftime("%Y-%m-%d")

def entry_exists(date_str):
    """Check if any journal entry exists for a given date."""
    ensure_journal_dir()
    return any(f.startswith(date_str) and f.endswith(FILE_EXT)
               for f in os.listdir(JOURNAL_DIR))

def entry_count_today():
    """Count how many entries exist for today."""
    ensure_journal_dir()
    ds = today_str()
    return sum(1 for f in os.listdir(JOURNAL_DIR)
               if f.startswith(ds) and f.endswith(FILE_EXT))

def list_entries():
    """Return list of entry filenames, newest first."""
    ensure_journal_dir()
    files = [f for f in os.listdir(JOURNAL_DIR)
             if f.endswith(FILE_EXT) and not f.startswith(".")]
    files.sort(reverse=True)
    return files

def read_entry(filename):
    """Read an entry's contents. Returns text or None."""
    try:
        with open(os.path.join(JOURNAL_DIR, filename), 'r', errors='replace') as f:
            return f.read()
    except Exception:
        return None

def get_week_dates():
    """Get Monday–Sunday dates for the current week."""
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())
    return [monday + timedelta(days=i) for i in range(7)]

def get_streak():
    """Count consecutive days with entries ending at yesterday or today."""
    today = datetime.now().date()
    streak = 0
    day = today
    while True:
        if entry_exists(day.strftime("%Y-%m-%d")):
            streak += 1
            day -= timedelta(days=1)
        else:
            break
    return streak

def get_total_entries():
    """Count total journal entries."""
    ensure_journal_dir()
    return len([f for f in os.listdir(JOURNAL_DIR)
                if f.endswith(FILE_EXT) and not f.startswith(".")])

def save_entry(text):
    """Save a journal entry as plain text."""
    ensure_journal_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    filepath = os.path.join(JOURNAL_DIR, f"{timestamp}{FILE_EXT}")
    with open(filepath, 'w') as f:
        f.write(text)
    return filepath

# ── UI Components ───────────────────────────────────────────────────────────

def draw_status(stdscr, left="", right="", style=None):
    h, w = stdscr.getmaxyx()
    if style is None:
        style = curses.A_REVERSE
    bar = left + " " * max(0, w - len(left) - len(right)) + right
    bar = bar[:w]
    try:
        stdscr.addstr(h - 1, 0, bar, style)
    except curses.error:
        pass

def draw_help_bar(stdscr, text):
    h, w = stdscr.getmaxyx()
    text = text[:w]
    try:
        stdscr.addstr(h - 2, 0, text + " " * max(0, w - len(text)), curses.A_DIM)
    except curses.error:
        pass

def prompt_input(stdscr, label):
    """Prompt for text input. Returns string or None on Esc."""
    curses.curs_set(1)
    h, w = stdscr.getmaxyx()
    buf = ""
    while True:
        display = f" {label}{buf}"
        try:
            stdscr.addstr(h - 1, 0, display + " " * max(0, w - len(display)),
                          curses.A_REVERSE)
            stdscr.move(h - 1, min(len(display), w - 1))
        except curses.error:
            pass
        stdscr.refresh()

        ch = stdscr.getch()
        if ch == 27:
            curses.curs_set(0)
            return None
        elif ch in (curses.KEY_ENTER, 10, 13):
            curses.curs_set(0)
            return buf.strip()
        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            buf = buf[:-1]
        elif 32 <= ch < 127:
            buf += chr(ch)

def confirm(stdscr, message):
    """Yes/no confirmation."""
    h, w = stdscr.getmaxyx()
    draw_status(stdscr, left=f" {message} (y/n)")
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch in (ord('y'), ord('Y')):
            return True
        if ch in (ord('n'), ord('N'), 27):
            return False

# ── Word Wrap ───────────────────────────────────────────────────────────────

def wrap_line(line, width):
    if width <= 0:
        return [(0, len(line))]
    if len(line) == 0:
        return [(0, 0)]
    segments = []
    pos = 0
    length = len(line)
    while pos < length:
        if length - pos <= width:
            segments.append((pos, length))
            break
        chunk_end = pos + width
        break_at = line.rfind(' ', pos, chunk_end)
        if break_at > pos:
            segments.append((pos, break_at))
            pos = break_at + 1
        else:
            segments.append((pos, chunk_end))
            pos = chunk_end
    return segments

def build_wrap_map(lines, width):
    vrows = []
    for li, line in enumerate(lines):
        segs = wrap_line(line, width)
        for start, end in segs:
            vrows.append((li, start, end))
    return vrows

def logical_to_visual(vrows, cy, cx):
    for vi, (li, scol, ecol) in enumerate(vrows):
        if li == cy and scol <= cx <= ecol:
            if cx == ecol and ecol > scol:
                if vi + 1 < len(vrows) and vrows[vi + 1][0] == li:
                    continue
            return vi, cx - scol
    if vrows:
        vi = len(vrows) - 1
        li, scol, ecol = vrows[vi]
        return vi, min(cx - scol, ecol - scol)
    return 0, 0

def visual_to_logical(vrows, vi, screen_cx):
    if not vrows:
        return 0, 0
    vi = max(0, min(vi, len(vrows) - 1))
    li, scol, ecol = vrows[vi]
    max_cx = ecol - scol
    screen_cx = max(0, min(screen_cx, max_cx))
    return li, scol + screen_cx

def word_count(lines):
    return sum(len(line.split()) for line in lines)

# ── Main Screen ─────────────────────────────────────────────────────────────

def draw_main_screen(stdscr, accent):
    """Draw the journal home screen with weekly tracker."""
    curses.curs_set(0)

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()

        week_dates = get_week_dates()
        today = datetime.now().date()
        today_count = entry_count_today()
        streak = get_streak()
        total = get_total_entries()

        # Title
        row = 1
        title = "journal"
        tx = max(0, (w - len(title)) // 2)
        try:
            stdscr.addstr(row, tx, title, curses.A_BOLD)
        except curses.error:
            pass

        # Weekly tracker
        row = 4
        day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

        header = "  "
        marks = "  "
        for i, d in enumerate(week_dates):
            dstr = d.strftime("%Y-%m-%d")
            is_today = (d == today)
            has_entry = entry_exists(dstr)

            name = day_names[i]
            if is_today:
                header += f"[{name}]"
            else:
                header += f" {name} "
            if i < 6:
                header += "  "

            if has_entry:
                marks += "  ✓  "
            elif d <= today:
                marks += "  ·  "
            else:
                marks += "     "
            if i < 6:
                marks += "  "

        hx = max(0, (w - len(header)) // 2)
        mx = max(0, (w - len(marks)) // 2)
        try:
            stdscr.addstr(row, hx, header, accent)
            stdscr.addstr(row + 1, mx, marks, curses.A_BOLD)
        except curses.error:
            pass

        # Stats
        row = 8
        stats = f"streak: {streak} day{'s' if streak != 1 else ''}  ·  total: {total} entr{'ies' if total != 1 else 'y'}"
        sx = max(0, (w - len(stats)) // 2)
        try:
            stdscr.addstr(row, sx, stats, curses.A_DIM)
        except curses.error:
            pass

        # Today's status
        row = 10
        if today_count > 0:
            if today_count == 1:
                status = "✓ 1 entry today"
            else:
                status = f"✓ {today_count} entries today"
            style = accent | curses.A_BOLD
        else:
            status = "no entry yet today"
            style = curses.A_DIM
        stx = max(0, (w - len(status)) // 2)
        try:
            stdscr.addstr(row, stx, status, style)
        except curses.error:
            pass

        # Menu — always visible
        row = 13
        opt1 = "[p] prompted write"
        opt2 = "[f] freewrite"
        opt3 = "[v] view past entries"
        o1x = max(0, (w - len(opt1)) // 2)
        o2x = max(0, (w - len(opt2)) // 2)
        o3x = max(0, (w - len(opt3)) // 2)
        try:
            stdscr.addstr(row, o1x, opt1)
            stdscr.addstr(row + 1, o2x, opt2)
            if total > 0:
                stdscr.addstr(row + 2, o3x, opt3)
        except curses.error:
            pass

        quit_opt = "[q] quit"
        qx = max(0, (w - len(quit_opt)) // 2)
        try:
            stdscr.addstr(row + 4, qx, quit_opt, curses.A_DIM)
        except curses.error:
            pass

        stdscr.refresh()
        ch = stdscr.getch()

        if ch == ord('q'):
            return None

        elif ch == ord('p'):
            return "prompt"

        elif ch == ord('f'):
            return "freewrite"

        elif ch == ord('v') and total > 0:
            return "view"

# ── Entry Browser & Viewer ──────────────────────────────────────────────────

def entry_browser(stdscr, accent):
    """Browse past entries. Returns filename to view, or None."""
    curses.curs_set(0)
    sel = 0
    scroll_off = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        usable = h - 3

        entries = list_entries()

        header = " past entries"
        try:
            stdscr.addstr(0, 0, (header + " " * w)[:w], curses.A_BOLD)
        except curses.error:
            pass

        if not entries:
            msg = "No entries yet."
            try:
                stdscr.addstr(h // 2, max(0, (w - len(msg)) // 2), msg, curses.A_DIM)
            except curses.error:
                pass
        else:
            sel = max(0, min(sel, len(entries) - 1))
            if sel < scroll_off:
                scroll_off = sel
            if sel >= scroll_off + usable:
                scroll_off = sel - usable + 1

            for i in range(usable):
                idx = scroll_off + i
                if idx >= len(entries):
                    break
                fname = entries[idx]
                # Parse date from filename: 2026-03-27_143022.txt
                date_part = fname.replace(FILE_EXT, '')
                try:
                    dt = datetime.strptime(date_part, "%Y-%m-%d_%H%M%S")
                    display_date = dt.strftime("%b %d, %Y  %H:%M")
                except ValueError:
                    display_date = date_part

                # Read first line of content for preview
                content = read_entry(fname)
                preview = ""
                if content:
                    # Skip metadata header to find actual writing
                    for line in content.split('\n'):
                        stripped = line.strip()
                        if stripped and not stripped.startswith(('DATE:', 'WORDS:', 'PROMPT:', 'FREEWRITE')):
                            preview = stripped[:w - len(display_date) - 10]
                            break
                    if not preview:
                        lines = [l.strip() for l in content.split('\n') if l.strip()]
                        if lines:
                            preview = lines[0][:w - len(display_date) - 10]

                row = i + 1
                if idx == sel:
                    style = curses.A_REVERSE
                    prefix = " › "
                else:
                    style = curses.A_NORMAL
                    prefix = "   "

                line = prefix + display_date
                if preview:
                    remaining = w - len(line) - 3
                    if remaining > 10:
                        line += "  " + preview[:remaining]
                line = line[:w]
                try:
                    stdscr.addstr(row, 0, line + " " * max(0, w - len(line)), style)
                except curses.error:
                    pass

        help_text = " [enter] read  [q] back"
        try:
            stdscr.addstr(h - 2, 0, (help_text + " " * w)[:w], curses.A_DIM)
        except curses.error:
            pass

        count = f"{len(entries)} entr{'ies' if len(entries) != 1 else 'y'}"
        draw_status(stdscr, left=" ~/journal", right=f"{count} ")

        stdscr.refresh()
        ch = stdscr.getch()

        if ch == ord('q') or ch == 27:
            return None
        elif ch == curses.KEY_UP or ch == ord('k'):
            sel = max(0, sel - 1)
        elif ch == curses.KEY_DOWN or ch == ord('j'):
            sel = min(max(0, len(entries) - 1), sel + 1)
        elif ch == curses.KEY_HOME:
            sel = 0
        elif ch == curses.KEY_END:
            sel = max(0, len(entries) - 1)
        elif ch in (curses.KEY_ENTER, 10, 13):
            if entries:
                return entries[sel]


def entry_viewer(stdscr, accent, filename):
    """Read-only pager for a journal entry."""
    curses.curs_set(0)

    content = read_entry(filename)
    if not content:
        return

    h, w = stdscr.getmaxyx()

    # Parse date for header
    date_part = filename.replace(FILE_EXT, '')
    try:
        dt = datetime.strptime(date_part, "%Y-%m-%d_%H%M%S")
        display_date = dt.strftime("%b %d, %Y  %H:%M")
    except ValueError:
        display_date = date_part

    # Build display lines
    lines = []
    lines.append({"text": "", "style": curses.A_NORMAL})
    lines.append({"text": f"  {display_date}", "style": accent | curses.A_BOLD})
    lines.append({"text": "", "style": curses.A_NORMAL})

    for raw_line in content.split('\n'):
        stripped = raw_line.strip()
        # Style metadata differently
        if stripped.startswith(('DATE:', 'WORDS:')):
            continue  # skip metadata, we show date in header
        elif stripped.startswith('PROMPT:'):
            prompt_text = stripped[7:].strip()
            wrapped = textwrap.fill(prompt_text, width=w - 6)
            for wl in wrapped.split('\n'):
                lines.append({"text": f"  {wl}", "style": accent | curses.A_DIM})
            lines.append({"text": "", "style": curses.A_NORMAL})
        elif stripped == 'FREEWRITE':
            lines.append({"text": "  freewrite", "style": curses.A_DIM})
            lines.append({"text": "", "style": curses.A_NORMAL})
        elif stripped == '':
            lines.append({"text": "", "style": curses.A_NORMAL})
        else:
            wrapped = textwrap.fill(raw_line, width=w - 4)
            for wl in wrapped.split('\n'):
                lines.append({"text": f"  {wl}", "style": curses.A_NORMAL})

    lines.append({"text": "", "style": curses.A_NORMAL})

    scroll = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        text_h = h - 2
        max_scroll = max(0, len(lines) - text_h)
        scroll = max(0, min(scroll, max_scroll))

        for i in range(text_h):
            line_idx = scroll + i
            if line_idx >= len(lines):
                break
            ld = lines[line_idx]
            try:
                stdscr.addstr(i, 0, ld["text"][:w - 1], ld.get("style", curses.A_NORMAL))
            except curses.error:
                pass

        # Status bar
        if len(lines) > text_h:
            pct = int((scroll / max(1, max_scroll)) * 100)
            pos = f" {pct}%"
        else:
            pos = " 100%"
        draw_status(stdscr, left=f" {display_date}  (read-only)", right=f"{pos} ")

        help_text = " ↑↓ scroll  g/G top/end  q:back"
        try:
            stdscr.addstr(h - 2, 0, (help_text + " " * w)[:w], curses.A_DIM)
        except curses.error:
            pass

        stdscr.refresh()
        ch = stdscr.getch()

        if ch == ord('q') or ch == 27:
            return
        elif ch == curses.KEY_UP or ch == ord('k'):
            scroll = max(0, scroll - 1)
        elif ch == curses.KEY_DOWN or ch == ord('j'):
            scroll = min(max_scroll, scroll + 1)
        elif ch == curses.KEY_PPAGE or ch == ord(' '):
            scroll = max(0, scroll - text_h)
        elif ch == curses.KEY_NPAGE:
            scroll = min(max_scroll, scroll + text_h)
        elif ch == ord('g'):
            scroll = 0
        elif ch == ord('G'):
            scroll = max_scroll


# ── Editor ──────────────────────────────────────────────────────────────────

def journal_editor(stdscr, accent, prompt_text=None):
    """
    Write-once journal editor.
    Returns the entry text, or None if cancelled with nothing written.
    """
    lines = ['']
    cx, cy = 0, 0
    scroll_y = 0
    target_screen_cx = None

    # Calculate prompt display height for offset
    prompt_lines = []
    prompt_h = 0
    if prompt_text:
        import textwrap
        h, w = stdscr.getmaxyx()
        wrapped = textwrap.fill(prompt_text, width=w - 6)
        prompt_lines = wrapped.split('\n')
        prompt_h = len(prompt_lines) + 3  # blank line + prompt lines + blank line + separator

    curses.curs_set(1)

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        text_h = h - 2 - prompt_h  # status + help + prompt area

        # Clamp cursor
        cy = max(0, min(cy, len(lines) - 1))
        cx = max(0, min(cx, len(lines[cy])))

        # Build wrap map
        vrows = build_wrap_map(lines, w)
        vi_cursor, scx_cursor = logical_to_visual(vrows, cy, cx)

        # Scroll
        if vi_cursor < scroll_y:
            scroll_y = vi_cursor
        if vi_cursor >= scroll_y + text_h:
            scroll_y = vi_cursor - text_h + 1
        scroll_y = max(0, min(scroll_y, max(0, len(vrows) - text_h)))

        # Draw prompt area at top
        draw_row = 0
        if prompt_text:
            draw_row += 1  # blank line
            for pl in prompt_lines:
                try:
                    stdscr.addstr(draw_row, 3, pl, accent | curses.A_DIM)
                except curses.error:
                    pass
                draw_row += 1
            draw_row += 1  # blank line
            # Thin separator
            sep = "─" * (w - 2)
            try:
                stdscr.addstr(draw_row, 1, sep, curses.A_DIM)
            except curses.error:
                pass
            draw_row += 1

        # Draw text
        for i in range(text_h):
            vi = scroll_y + i
            if vi >= len(vrows):
                break
            li, scol, ecol = vrows[vi]
            segment = lines[li][scol:ecol]
            try:
                stdscr.addstr(draw_row + i, 0, segment)
            except curses.error:
                pass

        # Help bar
        draw_help_bar(stdscr, " ^W finish & save  ^Q discard")

        # Status bar
        wc = word_count(lines)
        date_display = datetime.now().strftime("%b %d, %Y")
        mode = "prompted" if prompt_text else "freewrite"
        left = f" {date_display}  ·  {mode}"
        right = f"ln {cy + 1}/{len(lines)}  {wc}w "
        draw_status(stdscr, left=left, right=right)

        # Cursor
        screen_row = draw_row + (vi_cursor - scroll_y)
        try:
            stdscr.move(screen_row, scx_cursor)
        except curses.error:
            pass

        stdscr.refresh()
        ch = stdscr.getch()
        continue_sticky = False

        # ── Navigation ──

        if ch == curses.KEY_UP:
            if vi_cursor > 0:
                if target_screen_cx is None:
                    target_screen_cx = scx_cursor
                cy, cx = visual_to_logical(vrows, vi_cursor - 1, target_screen_cx)
            continue_sticky = True

        elif ch == curses.KEY_DOWN:
            if vi_cursor < len(vrows) - 1:
                if target_screen_cx is None:
                    target_screen_cx = scx_cursor
                cy, cx = visual_to_logical(vrows, vi_cursor + 1, target_screen_cx)
            continue_sticky = True

        elif ch == curses.KEY_LEFT:
            if cx > 0:
                cx -= 1
            elif cy > 0:
                cy -= 1
                cx = len(lines[cy])

        elif ch == curses.KEY_RIGHT:
            if cx < len(lines[cy]):
                cx += 1
            elif cy < len(lines) - 1:
                cy += 1
                cx = 0

        elif ch == curses.KEY_HOME:
            li, scol, ecol = vrows[vi_cursor]
            cx = scol

        elif ch == curses.KEY_END:
            li, scol, ecol = vrows[vi_cursor]
            cx = ecol

        elif ch == curses.KEY_PPAGE:
            target_vi = max(0, vi_cursor - text_h)
            if target_screen_cx is None:
                target_screen_cx = scx_cursor
            cy, cx = visual_to_logical(vrows, target_vi, target_screen_cx)
            continue_sticky = True

        elif ch == curses.KEY_NPAGE:
            target_vi = min(len(vrows) - 1, vi_cursor + text_h)
            if target_screen_cx is None:
                target_screen_cx = scx_cursor
            cy, cx = visual_to_logical(vrows, target_vi, target_screen_cx)
            continue_sticky = True

        # ── Editing ──

        elif ch in (curses.KEY_BACKSPACE, 127, 8):
            if cx > 0:
                lines[cy] = lines[cy][:cx - 1] + lines[cy][cx:]
                cx -= 1
            elif cy > 0:
                cx = len(lines[cy - 1])
                lines[cy - 1] += lines[cy]
                lines.pop(cy)
                cy -= 1

        elif ch == curses.KEY_DC:
            if cx < len(lines[cy]):
                lines[cy] = lines[cy][:cx] + lines[cy][cx + 1:]
            elif cy < len(lines) - 1:
                lines[cy] += lines[cy + 1]
                lines.pop(cy + 1)

        elif ch in (curses.KEY_ENTER, 10, 13):
            rest = lines[cy][cx:]
            lines[cy] = lines[cy][:cx]
            cy += 1
            lines.insert(cy, rest)
            cx = 0

        elif ch == 9:  # Tab
            spaces = " " * TAB_WIDTH
            lines[cy] = lines[cy][:cx] + spaces + lines[cy][cx:]
            cx += TAB_WIDTH

        # ── Commands ──

        elif ch == 23:  # Ctrl+W — finish & save
            text = '\n'.join(lines).strip()
            if not text:
                curses.curs_set(0)
                return None
            curses.curs_set(0)
            return text

        elif ch == 17:  # Ctrl+Q — discard
            text = '\n'.join(lines).strip()
            if text:
                if confirm(stdscr, "discard this entry?"):
                    curses.curs_set(0)
                    return None
                curses.curs_set(1)
            else:
                curses.curs_set(0)
                return None

        elif ch == 27:  # Esc — same as Ctrl+Q
            text = '\n'.join(lines).strip()
            if text:
                if confirm(stdscr, "discard this entry?"):
                    curses.curs_set(0)
                    return None
                curses.curs_set(1)
            else:
                curses.curs_set(0)
                return None

        # ── Printable ──

        elif 32 <= ch <= 126:
            lines[cy] = lines[cy][:cx] + chr(ch) + lines[cy][cx:]
            cx += 1

        if not continue_sticky:
            target_screen_cx = None

# ── Main ────────────────────────────────────────────────────────────────────

def main(stdscr):
    curses.raw()
    stdscr.keypad(True)
    curses.use_default_colors()
    curses.set_escdelay(25)
    curses.curs_set(0)

    # Colors
    curses.init_pair(1, curses.COLOR_YELLOW, -1)
    accent = curses.color_pair(1)

    ensure_journal_dir()

    while True:
        action = draw_main_screen(stdscr, accent)

        if action is None:
            break

        if action == "view":
            # Browse and view past entries
            while True:
                filename = entry_browser(stdscr, accent)
                if filename is None:
                    break
                entry_viewer(stdscr, accent, filename)
            continue

        # Select prompt
        if action == "prompt":
            prompt_text = random.choice(PROMPTS)
        else:
            prompt_text = None

        # Write entry
        text = journal_editor(stdscr, accent, prompt_text=prompt_text)

        if text is None:
            continue

        # Prepend prompt to saved text if applicable
        if prompt_text:
            full_text = f"PROMPT: {prompt_text}\n\n{text}"
        else:
            full_text = f"FREEWRITE\n\n{text}"

        # Add metadata
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        wc = len(text.split())
        header = f"DATE: {timestamp}\nWORDS: {wc}\n\n"
        full_text = header + full_text

        save_entry(full_text)


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    print("bye.")
