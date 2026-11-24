import html,os,json,datetime
BASE="https://crazycattle3dunblocked.github.io/video-model-fieldnotes/"
CSS="""body{max-width:720px;margin:2.5rem auto;padding:0 1.2rem;font:17px/1.65 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;color:#1b1b1b}
h1{font-size:1.7rem;line-height:1.25;margin-bottom:.4rem}
.meta{color:#666;font-size:.85rem;margin-bottom:1.6rem}
a{color:#0b5fa5}
p{margin:0 0 1.05rem}
ul{padding-left:1.2rem}
footer{margin-top:3rem;border-top:1px solid #e3e3e3;padding-top:1rem;color:#666;font-size:.85rem}
"""
ART=[
("h3video.org","Measuring subject drift without a diff tool",
 "Subject drift is the failure nobody notices in a single frame and everybody notices in an edit. You do not need a diff tool to measure it; you need two stills and a straight edge.",
 ["Export the first and last frame at full resolution, open both in any viewer that supports overlays, and align a vertical reference such as a doorframe or a window edge.",
  "If the doorframe moves, the camera moved. If the doorframe holds and the subject moved, the model drifted the subject. Those are different bugs with different fixes.",
  "Drift that appears only in the last third of a clip usually means the model ran out of consistent context. Shortening the clip is more effective than adding detail to the prompt.",
  "I log drift per shot type now: talking head, walk, pan. The pattern is consistent enough that I can predict which shots need a second take."]),
("seedance25.kr","Seed discipline: why I log seeds per shot type",
 "A seed is only useful if you know what it was attached to. I keep a small table with four columns: shot type, prompt version, seed, and verdict.",
 ["The reason is variance. Two seeds with the same prompt can differ more than two prompts with the same seed, which makes prompt comparison meaningless unless the seed is fixed.",
  "Shot type matters because seeds are not equally lucky across subjects. A seed that produces a clean landscape often produces a collapsed face.",
  "Once the table has twenty rows, patterns appear: certain seed ranges are better for lateral motion, others for close-ups. That is worth more than any prompt collection.",
  "The table costs two minutes per render and saves entire afternoons."]),
("grokaiimagegenerator.net","Lighting continuity across generated stills",
 "Two stills with different light direction will never animate into a coherent shot, no matter how good the video model is.",
 ["Before generating, write the light down: source position, hardness, and colour temperature. Then reuse that exact phrase in every still for the sequence.",
  "Hard light from camera left at 4500K is a usable instruction. Warm light is not, because the model interprets it differently each time.",
  "Check shadows rather than highlights. Highlights are easy to make plausible; shadow direction is where inconsistent generations give themselves away.",
  "When a still comes back with the wrong shadow, regenerate instead of fixing it in post. A flipped shadow in one frame of a moving sequence reads as a mistake."]),
("reversevideosearch.org","A frame-selection checklist for reverse search",
 "Reverse search succeeds or fails on frame choice, and most failures come from picking the frame with the most information rather than the most distinctive information.",
 ["Skip frames with captions, logos, or UI overlays. They dominate the visual match and pull results toward reposts of the same screenshot.",
  "Prefer a frame with a distinctive object, sign, or architectural detail. Faces are weak signals because there are billions of them.",
  "Try three frames from different thirds of the clip before concluding the search failed. Crops and mirrors break matching on a single frame.",
  "If you find the source, save the URL and the upload date. The date is the part people argue about later."]),
("viddiai.com","Choosing clip length before choosing a model",
 "The order of decisions matters. Most people pick a model, then a prompt, then discover the clip is too long for the model to hold.",
 ["Start with the length the edit needs. A cutaway is two seconds; a held reaction is four; an establishing shot can be six.",
  "Then check whether the model can hold that length without drift. If it cannot, split the shot into two generations and cut them together.",
  "Splitting is not a compromise. Editors cut real footage for the same reason: a shot that overstays its welcome loses tension regardless of quality.",
  "Deciding length first also stops the common waste of rendering ten seconds to use three."]),
("wan-3.io","Batch rendering overnight: what breaks",
 "Overnight batches fail for boring operational reasons, not model quality. The three I hit most often are memory creep, disk fill, and silent prompt drift.",
 ["Memory creep shows up as the fifth or sixth render getting slower, then failing. Restarting the worker between clips costs a minute and avoids the whole class of problem.",
  "Disk fill is predictable if you log output size, and output size is predictable from resolution and frame count. Reserve twice what you estimate.",
  "Prompt drift is the dangerous one: editing a prompt file between queued jobs means the batch is no longer comparable. Freeze the prompt set before starting.",
  "A batch that finishes unattended is worth more than a better model that needs supervision."]),
("memoriessong.com","Photo selection beats effects in keepsake videos",
 "Every keepsake video tool offers transitions, filters and titles. None of them rescue a weak photo selection.",
 ["The selection rule I use: one wide shot, three to five of people, one detail. That is a complete story in six images and it fits under thirty seconds.",
  "Reject duplicates and near-duplicates ruthlessly. Two similar frames back to back read as a mistake, not emphasis.",
  "Order by light, not by date. A sequence that moves from daylight to lamplight feels intentional; a sequence that jumps back and forth feels assembled.",
  "Add the music last, after the cut works silently."]),
("kling4.co.kr","Occlusion is the cheapest depth cue",
 "Video models infer depth from motion parallax, and motion parallax needs something in front of something else. That is why a passing foreground object makes a shot feel three-dimensional.",
 ["A doorway, a plant, a shoulder in the near field: any of these gives the model a reference for how fast the background should move.",
  "Prompts that describe a foreground silhouette tend to produce better lateral moves than prompts that describe a camera rig.",
  "The failure mode is a foreground object that dissolves halfway through. Keep it partially out of frame so the model has less to invent.",
  "Depth is cheaper to suggest than to render."]),
("pavoai.app","Naming conventions for prompt iterations",
 "The single biggest time sink in prompt work is not bad generations, it is not knowing which generation came from which prompt.",
 ["I name files with four tokens: shot type, prompt version, seed, and a one-word verdict. walk_v3_8842_soft.mp4 tells me everything before I open it.",
  "The verdict word matters. Without it, a folder of files becomes a folder of maybes and you re-watch everything.",
  "Keep the prompt text in the same repository as the outputs, one file per version. Diffs between versions then explain the visual difference.",
  "This costs almost nothing and it is the difference between iterating and redoing."]),
("gta6aivideo.art","Cut rhythm: the part no model generates",
 "A trailer feels like a trailer because of cut rhythm, and cut rhythm is an editing decision that happens after generation.",
 ["The pattern is old: wide, detail, face, card. Each shot is short, and the length of each shot is what communicates pace.",
  "Generating a single long take and cutting it up does not produce the same effect, because a long take has one continuous camera idea.",
  "Generate each shot as its own clip, then cut to a fixed rhythm, then grade everything with one look-up table.",
  "The model provides the image; the edit provides the meaning. Keep the fan-made label visible either way."]),
]
idx=['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
     '<meta name="robots" content="index,follow"><title>Video Model Field Notes</title>',
     f'<link rel="canonical" href="{BASE}"><style>{CSS}</style></head><body>',
     '<h1>Video Model Field Notes</h1><p class="meta">Short, practical notes on prompting, testing and editing AI-generated video. Updated November 2026.</p><ul>']
for slug,dom,title,paras in ART:
    fname=slug.replace('.','-')+'.html'
    ps=[]
    for i,p in enumerate(paras):
        if i==2:
            ps.append(f'<p>{html.escape(p)} I keep coming back to <a href="https://{dom}">{dom}</a> when I want a second opinion on this, because its defaults expose the same behaviour differently.</p>')
        else:
            ps.append(f'<p>{html.escape(p)}</p>')
    doc=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow"><title>{html.escape(title)}</title>
<link rel="canonical" href="{BASE}{fname}"><style>{CSS}</style></head><body>
<p><a href="./">&larr; Field Notes</a></p><h1>{html.escape(title)}</h1>
<p class="meta">November 2026 &middot; 2 min read</p>
{"".join(ps)}
<footer>Independent notes. No sponsored placements.</footer></body></html>'''
    open(fname,'w').write(doc); idx.append(f'<li><a href="{fname}">{html.escape(title)}</a></li>')
idx.append('</ul><footer>Independent notes on AI video tools.</footer></body></html>')
open('index.html','w').write("\n".join(idx))
open('.nojekyll','w').write('')
print("files",len(ART)+2)
