import bpy, time, os, shutil

# BVH 파일 저장 경로
bvh_folder_path = "C:/Users/054/Desktop/BVH_files"
files = [f for f in os.listdir(bvh_folder_path) if os.path.isfile(os.path.join(bvh_folder_path, f))]

# 메인 캐릭터, 시작 애니메이션 파일 위치는 BVH 파일 폴더와 다른 곳이어야 함
adot = bpy.data.objects.get("HelloBlender") # 기본 캐릭터 
adot_name = "HelloBlender"
first_anim_path = "C:/Users/054/Desktop/Temp_bvh/HelloBlender.bvh"

# BVH 파일 저장 폴더 비우기
for filename in os.listdir(bvh_folder_path):
    file_path = os.path.join(bvh_folder_path, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"파일 삭제: {file_path}")
    except Exception as e:
        print(f"파일 삭제 실패: {file_path}, 오류: {e}")

def play_animation():
    bpy.ops.screen.animation_play()
    
def stop_animation():
    bpy.ops.screen.animation_cancel()

def get_animation_delete(bvh_path): # BVH파일을 블랜더 scene에 임포트, 기존 armature 삭제
    global adot, cur_animation
    bpy.ops.import_anim.bvh(filepath=bvh_path)
    armature_name = bvh_path.split("/")[-1]
    armature_name = armature_name.split(".")[0]
    for obj in bpy.context.scene.objects:
        if obj.type == 'ARMATURE' and obj.name != armature_name:
            bpy.data.objects.remove(obj, do_unlink=True)

animation_on = True

def main_timer():
    global bvh_folder_path, files, animation_on, adot, anilist
    print(int((time.time()-startTime)*10)/10, end="\r") # 프로그램 켜놓은 시간 체크
    files = [f for f in os.listdir(bvh_folder_path) if os.path.isfile(os.path.join(bvh_folder_path, f))]
    if len(files) > 1:
        files.sort(key=lambda f: os.path.getmtime(os.path.join(bvh_folder_path, f)))
        old_file_path = os.path.join(bvh_folder_path, files[0]).replace('\\', '/')
        os.remove(old_file_path)
        animation_on = True
    if animation_on and len(files) == 1:
        animation_on = False
        stop_animation()
        nowpath = os.path.join(bvh_folder_path, files[0]).replace('\\', '/')
        get_animation_delete(nowpath)
        bpy.app.timers.register(restart_animation, first_interval=0.075)
    
    return 0.05 # 타이머 간격 (초)

def restart_animation():
    global adot, anilist, cur_animation
    bpy.app.timers.unregister(restart_animation)
    play_animation()

# 타이머 등록, 타이머 간격을 주기로 update반복
bpy.app.timers.register(main_timer)
startTime = time.time()
get_animation_delete(first_anim_path) 
play_animation()