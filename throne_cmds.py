from time import sleep
import pyperclip, os, threading
from difflib import SequenceMatcher

def areSimilar(a,b):
    return SequenceMatcher(None, a, b).ratio()>0.8


## execution function
def execCmd(citidel, mel, language, face, davos, lf, bran, luwin, action, getCmdData, kill_and_raise):
    try:
        print ('gonna exec', action)
        if(action=='raise'):
            luwin.new_event('raise')
            mod=getCmdData(action)
            luwin.in_event('raise',mod)
            kill_and_raise(mod)
            luwin.end_event()
            return 1
        if(areSimilar("listen to the king",action)):
            luwin.new_event('listen to the king')
            luwin.end_event()
            return 1
        if(areSimilar("get me these lyrics",action)):
            luwin.new_event('song lyrics download')
            song=pyperclip.paste()
            link=mel.getYoutubeBestSearch(song+" lyrics")
            luwin.in_event(song)
            download_thread=threading.Thread(target=mel.downloadAudioFrom, args=(link,))
            download_thread.start()
            luwin.end_event()
            return 1
        if(areSimilar("get me this song",action)):
            luwin.new_event('song name download')
            song=pyperclip.paste()
            if('youtube.com' not in song):
                song=getCmdData(action)
            luwin.in_event(song)
            if(song):
                if('youtube.com' not in song):
                    link=mel.getYoutubeBestSearch(song)
                else:
                    link=song
                download_thread=threading.Thread(target=mel.downloadAudioFrom, args=(link,))
                download_thread.start()
                luwin.in_event(song)
                luwin.end_event()
            return 1
        if(action[0] in ('+','-')):
            luwin.new_event('money log')
            details=getCmdData(action)
            luwin.in_event(action,details)
            target=getCmdData(details)
            luwin.in_event(action,details, target)
            if('salary' in details.lower()):
                lf.add_salary(action,target)
                return 1
            lf.add_log(action, target, details)
            luwin.end_event()
            return 1
        elif(action[0] == '$'):
            luwin.new_event('money transfer')
            action=action[1:]
            src=getCmdData('$'+action)
            luwin.in_event(action, src)
            trgt=getCmdData(src)
            luwin.in_event(action, src, trgt)
            lf.do_transfer(action,src,trgt)
            luwin.end_event()
            return 1
        if(areSimilar("duck, find me this",action)):
            luwin.new_event('ducky search')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query)
            luwin.end_event()
            return 1
        if(areSimilar("get the meaning of",action)):
            luwin.new_event('meaning fetch')
            word=getCmdData(action)
            luwin.in_event(word)
            word=language.get_word(word.lower())
            data='\n'.join(word.meanings)
            if(not len(data)):
                citidel.info_data="No books in the citidel have this."
                sleep(0.1)
                return 1
            citidel.info_data=data
            sleep(0.1)
            luwin.end_event()
            return 1
        if(areSimilar("tree mode",action)):
            luwin.new_event("tree mode")
            cmd=getCmdData(action)
            get_down=False
            path_list_needed=True
            path_list_refresh=True
            while(not get_down):
                if(areSimilar(cmd,'switch mode')):
                    get_down=True
                    continue
                if(path_list_needed):
                    trgt=cmd.lower()
                    bran.choose_tree(trgt)
                    pathList=bran.tree.all_leaves
                if(len(pathList) and path_list_refresh):
                    citidel.ui_scroller_data=pathList
                    citidel.ui_scroller=True
                cmd=getCmdData(action)
                path_list_refresh=True
                path_list_needed=True
                if(cmd[1:] in bran.tree.file_leaves or cmd[2:] in bran.tree.file_leaves):
                    path_list_refresh=False
                    path_list_needed=False
                    continue
                if(len(cmd)>1 and cmd[0]=='|' and cmd[1]!='.'):
                    if(bran.conflict):
                        bran.conflict=False
                        path_list_needed=False
                        bran.tree.tree=[branch for branch in cmd[1:].split('\\') if branch]
                        pathList=bran.tree.get_all_leaves()
                    else:
                        if(not cmd[1:] in bran.tree.file_leaves):
                            bran.tree.climb_up(cmd[1:])
                            pathList=bran.tree.get_all_leaves()
                            path_list_needed=False

                if(cmd[:2]=='>>'):
                    if(not cmd[2:] in bran.tree.file_leaves):
                        bran.get_inside(cmd[2:])
                        path_list_needed=False
                        path_list_refresh=False
                if(cmd[1:3]=='..'):
                    if(len(bran.tree.tree)>1):
                        bran.tree.move_down_branch()
                        pathList=bran.tree.get_all_leaves()
                    path_list_needed=False
            citidel.ui_scroller=True
            citidel.ui_scroller_data=[]
            sleep(0.2)
            luwin.end_event()

        if(areSimilar("open this",action)):
            luwin.new_event('open this')
            trgt=getCmdData(action)
            trgt=trgt.lower()
            luwin.in_event(trgt)
            if(len(bran.show_glimpse(trgt))==1):
                bran.get_inside(bran.get_path(trgt))
            luwin.end_event()
        if(areSimilar("get word data",action)):
            luwin.new_event('word data')
            word=getCmdData(action)
            luwin.in_event(word)
            word=language.get_word(word.lower())
            data_m='\n'.join(word.meanings)
            data_sy='\n'.join(word.synonyms)
            data_sn='\n'.join(word.sentences)
            citidel.info_data='It may mean any of the following.'
            sleep(0.1)
            citidel.info_data=data_m
            sleep(0.1)
            citidel.info_data='Do you need the synonyms? Enter more for more info.'
            sleep(0.1)
            need=getCmdData(word.word)
            if(need=='more'):
                citidel.info_data=data_sy
                sleep(0.1)
                citidel.info_data='Do you need some example sentences? Enter more for more info.'
                sleep(0.1)
                need=getCmdData(need)
                if(need=='more'):
                    citidel.info_data=data_sn
                    sleep(0.1)
            luwin.end_event()
            return 1
        if(areSimilar("duck, work secretly",action)):
            luwin.new_event('duck incog')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query,incog=True)
            luwin.end_event()
            return 1
        if(areSimilar("take lang test",action)):
            luwin.new_event('new lang test')
            test_ques= language.init_test()
            test_ans=[]
            wronged=[]
            score=0
            for ques in test_ques:
                citidel.ui_scroller_data=language.get_options(ques[1])
                citidel.ui_scroller=True
                citidel.header_data=ques[0]
                cmd=getCmdData(action)
                if(len(cmd)>1 and cmd[0]=='|' and cmd[1]!='.'):
                    if(cmd[1:]==ques[1]):
                        score+=1
                        language.have_this_in_mind(ques[0])
                    else:
                        wronged+=[ques]
                if(cmd[1:3]=='..'):
                    language.mark_as_irrelevent(ques[0])

            citidel.ui_scroller=True
            citidel.ui_scroller_data=[]
            sleep(0.2)
            # citidel.header_data='You Scored ' + str(score) + ' point'+('s'*(not score == 1))+'.'
            citidel.info_data='You Scored ' + str(score) + ' point'+('s'*(not score == 1))+'.'
            sleep(0.1)
            for word in wronged:
                citidel.info_data='The word ' + word[0] + ' means '+word[1]
                sleep(0.1)


            luwin.end_event()
            return 1
        if(areSimilar("goo, find me this",action)):
            luwin.new_event('google this')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query,goo=True)
            luwin.end_event()
            return 1
        if(areSimilar("goo work secretly",action)):
            luwin.new_event('google incog')
            query=getCmdData(action)
            luwin.in_event(query)
            mel.get_info_on(query=query,goo=True,incog=True)
            luwin.end_event()
            return 1
        if(areSimilar("calculate exp",action)):
            luwin.new_event('calculating exp')
            pyperclip.copy(mel.calculate_this(pyperclip.paste()))
            luwin.end_event()
            return 1
        if(areSimilar("survey the world",action)):
            luwin.new_event('new survey')
            new_found=bran.new_happenings()
            while(len(new_found)):
                citidel.ui_scroller_data=new_found
                citidel.ui_scroller=True
                cmd=getCmdData(action)
                if(cmd=='put this on hold'):
                    break
                if(cmd=='let them be'):
                    bran.register_happenings()
                    new_found=[]
                ## TODO handle all inputs
                if(len(cmd)>1 and cmd[0]=='|' and cmd[1]!='.'):
                    new_found=bran.register_happening(cmd[1:])

            citidel.ui_scroller=True
            citidel.ui_scroller_data=[]
            sleep(0.2)
            luwin.end_event()
            return 1
        return 0
    except Exception as e:
        luwin.log_err(e)
        sleep(0.1)
