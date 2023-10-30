from django.shortcuts import render
from .models import Recording
from django.http import HttpResponse
# import pandas as pd
import datetime
import os


REC_PER_PAGE = 15

# Create your views here.
def search_view(request):
    # 获取请求参数(GET or POST)
    if request.method == "POST":
        form = request.POST
    else:
        form = request.GET

    # 如果没有page参数，设置page为1
    if "page" in form:
        page = int(form["page"])
    else:
        page = 1

    start_page = ((page - 1) // REC_PER_PAGE) * REC_PER_PAGE + 1
    end_page = start_page + REC_PER_PAGE - 1
    
    # 获取起始日期和结束日期，如没有，都设置为空字符串
    start_date = form["start_date"] if "start_date" in form else ""
    end_date = form["end_date"] if "end_date" in form else ""
    agent_id = form["agent_id"] if "agent_id" in form else ""
    duration = form["duration"] if "duration" in form else ""

    # 只要填写了任意一个条件，就搜索并展示录音
    if start_date or end_date or agent_id or duration:
        all_recordings = Recording.objects.all()

        # 如有起始日期，获取所有对应录音
        if start_date:
            all_recordings = all_recordings.filter(start_time__date__gte=datetime.date.fromisoformat(start_date))

        # 如有结束日期，获取所有对应录音
        if end_date:
            all_recordings = all_recordings.filter(start_time__date__lte=datetime.date.fromisoformat(end_date))

        # 如有座席ID，获取所有对应录音
        if agent_id:
            all_recordings = all_recordings.filter(agent_id__exact=agent_id)

        # 如有通话时长范围，获取所有对应录音
        if duration:
            if duration == "小于1分钟":
                all_recordings = all_recordings.filter(duration__lt=60)
            elif duration == "1分钟到5分钟":
                all_recordings = all_recordings.filter(duration__gte=60).filter(duration__lt=300)
            elif duration == "5分钟到10分钟":
                all_recordings = all_recordings.filter(duration__gte=300).filter(duration__lt=600)
            elif duration == "大于10分钟":
                all_recordings = all_recordings.filter(duration__gte=600)
            else:
                pass
    else:
        all_recordings = []


    # all_recordings = all_recordings[:200]
    
    # 计算总页数
    num_page = (len(all_recordings)-1) // REC_PER_PAGE + 1
    end_page = end_page if end_page <= num_page else num_page

    start_page_list = [page+1 for page in range(num_page) if page % REC_PER_PAGE == 0]

    # 生成当前页面的录音
    recordings = all_recordings[(page-1) * REC_PER_PAGE: page * REC_PER_PAGE]

    # 获取选中播放的单条录音
    if "file_name" in form:
        current_recording = Recording.objects.filter(file_name__startswith=str(form["file_name"]))[0]
    else:
        current_recording = None

    # 获取所有座席ID (去重)
    if all_recordings:
        all_agent_id = all_recordings.values("agent_id")
    else:
        all_agent_id = Recording.objects.values("agent_id")

    all_agent_id = set([item["agent_id"] for item in all_agent_id])

    context = {
        "num_recordings": len(all_recordings),
        "all_agent_id": all_agent_id,
        "recordings": recordings,
        "num_page": num_page,
        "start_page_list": start_page_list,
        "page_range": range(start_page, end_page + 1),
        "current_page": page,
        "index_of_page": (page-1)*REC_PER_PAGE,
        "current_recording": current_recording,
        "start_date": start_date,
        "end_date": end_date,
        "agent_id": agent_id,
        "duration": duration,
        "rec_per_page": REC_PER_PAGE,
    }
    return render(request, "search_playback/search.html", context=context)

def import_view(request):
    # df = pd.read_excel("search_playback\static\search_playback\metadata.xlsx")
    # for idx, rec in list(df.iterrows()):
    #     recording = Recording(
    #         file_name = rec["Filename"],
    #         start_time = datetime.now(),
    #         duration = rec["Duration"],
    #         direction = rec["direction"],
    #         extension = rec["extension"],
    #         agent_id = rec["agent_name"],
    #         ani = rec["ani"],
    #         dnis = rec["dnis"],
    #     )
    #     recording.save()

    return render(request, "search_playback/import.html")