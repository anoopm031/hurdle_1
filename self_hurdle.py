import pygame
import random
import math
#import datetime


'''initializing pygame and screen'''

pygame.init()
width=800
depth=800
screen= pygame.display.set_mode((width,depth))
pygame.display.set_caption("Self Hurdle")
icon=pygame.image.load("download.png")
pygame.display.set_icon(icon)


#Block class

class Block:
    def __init__(self, current_pos,checkp_no_1,direction):
        self.current_pos=current_pos
        #self.next_pos=next_pos
        self.checkp_no=checkp_no_1-1
        self.checkpoint_=checkp_list[checkp_no_1]
        self.checkp_valid=True

        self.direct=direction
        self.draw_block()



    def get_current_pos(self):
        return self.current_pos

    def get_checkp_no(self):
        return self.checkp_no

    def get_direct(self):
        return self.direct

    def move_block(self,next_pos_1):
        self.current_pos=self.next_pos   #to save the block_pos before changing it
        self.next_pos_1=next_pos_1
        self.next_pos=self.next_pos_1
        #pos=self.current_pos
        self.draw_block()

    def move_block_checkp(self,father_block_dir):
        if self.checkp_no> len(checkp_list)-1:
            self.direct = father_block_dir
            #self.checkp_valid = False
            self.current_pos = head_move(self.current_pos, self.direct)
            self.current_pos = check_boundary(self.current_pos)
            #print("I am except")
            self.draw_block()
        else:
            self.move_block_with_checkp()

        checkp_current_dist = math.sqrt((self.checkpoint_[0] - self.current_pos[0]) ** 2 + (self.checkpoint_[1] - self.current_pos[1]) ** 2)
        if checkp_current_dist<2 and self.checkp_no<len(checkp_list):
            self.checkp_no+=1


    def move_block_with_checkp(self):
        if self.checkpoint_[1]-self.current_pos[1]!=0:
            #motion in y direction
            if self.checkpoint_[1]-self.current_pos[1]>0:
                #movement in down y
                self.current_pos=[self.current_pos[0],self.current_pos[1]+snake_speed]
                self.direct="down"
            if self.checkpoint_[1] - self.current_pos[1] < 0:
                #movement in up y
                self.current_pos = [self.current_pos[0], self.current_pos[1]-snake_speed]
                self.direct = "up"
        if self.checkpoint_[0] - self.current_pos[0] != 0:
            #motion in x direction
            if self.checkpoint_[0]-self.current_pos[0]>0:
                #movement in right x
                self.current_pos=[self.current_pos[0]+snake_speed,self.current_pos[1]]
                self.direct = "right"
            if self.checkpoint_[0] - self.current_pos[0] < 0:
                #movement in left x
                self.current_pos = [self.current_pos[0]-snake_speed, self.current_pos[1]]
                self.direct = "left"
        #check boundary
        self.current_pos=check_boundary(self.current_pos)

        self.draw_block()

    def draw_block(self):
        color_blk = (255, 0,0)
        blk_size = 10
        draw_cicle(self.current_pos,color_blk,blk_size)
        #pygame.display.flip()






'''head'''

#function to generate the head at the starting of the game
def head_gen():
    color_head=(0,25,150)
    head_x_in = random.randint(2,798)
    head_y_in=random.randint(2,798)
    head_in_pos=[head_x_in,head_y_in]
    pygame.draw.circle(screen,color_head,head_in_pos,10)
    #pygame.display.flip()
    return  head_in_pos

#function to move the head as per the cordinates given
def head_move(head_pos, dir_):
    #print("head_move initiated")
    if dir_== "up":
        head_pos[1]-=snake_speed
    if dir_== "down":
        head_pos[1]+=snake_speed
    if dir_== "left":
        head_pos[0]-=snake_speed
    if dir_== "right":
        head_pos[0]+=snake_speed
    return head_pos



'''reward'''

#function to generate reward at random points
def reward_gen():
    rew_x_in = random.randint(2,798)
    rew_y_in=random.randint(2,798)
    rew_in_pos=[rew_x_in,rew_y_in]
    return  rew_in_pos



'''Drawing'''

#this function draws circles taking position,color and radius as inputs
def draw_cicle(pos,color,radius):
    pygame.draw.circle(screen,color,pos,radius)
    #pygame.display.flip()
    return 1

def draw_rect(pos,color,radius):
    pygame.draw.rect(screen,color,pygame.Rect(pos[0],pos[1],2*radius,2*radius))
    #pos_bottom=(pos[0]-5,pos[1]-5)
    #pos_top=(pos[0]-5,pos[1]+5)
    #pygame.display.update(rectangle=pygame.Rect(pos_bottom,pos_top,15,15))
    return


'''keeping snake inside the boundary'''
def check_boundary(point):
    '''to check the boundary and correct it'''
    if point[0]>800:
        point[0]=0
    if point[0]<0:
        point[0]=800
    if point[1]>800:
        point[1]=0
    if point[1]<0:
        point[1]=800
    return point


'''moving the body blocks'''
def move_body(score):
    for blk_no in range(1,score+1):
        if blk_no==1:
            father_block_dir=dir_
        else:
            father_block_name="block_{}".format(blk_no-1)
            father_block_dir=new_block_dict[father_block_name].get_direct()
        blk_now="block_{}".format(blk_no)
        new_block_dict[blk_now].move_block_checkp(father_block_dir)
        block_pos=new_block_dict[blk_now].get_current_pos()
        blk_head_dist=math.sqrt((block_pos[0]-head_pos[0])**2+(block_pos[1]-head_pos[1])**2)
        if blk_head_dist<size_head+3:
            game_over=True
            pygame.mixer.Sound.play(game_over_sound)
            game_state=game_over_msg()
            if game_state==0:
                running=False
            print(game_over)





'''creating the body block each time a reward is hit'''
def create_body_block(score,dirc,checkp_num):

    # head_pos_next=head_move(head_pos, dir_)
    #checkp_list.insert(checkp_no, head_pos.copy())
    if score==1:
        if dirc=="up":
            current_pos_ini=[head_pos[0],head_pos[1]+2*size_head]
        if dirc=="down":
            current_pos_ini = [head_pos[0], head_pos[1] - 2*size_head]
        if dirc == "left":
            current_pos_ini = [head_pos[0]+2*size_head, head_pos[1]]
        if dirc == "right":
            current_pos_ini = [head_pos[0] - 2*size_head, head_pos[1]]

        current_checkp=checkp_num
        block_create_name="block_{}".format(score)
        #print("body create",checkp_list)
        new_block_dict[block_create_name]=Block(current_pos_ini,current_checkp,dirc)
    if score>1:
        fath_block_name="block_{}".format(score-1)
        fath_block=new_block_dict[fath_block_name]
        start_pos=fath_block.get_current_pos()
        if dirc=="up":
            current_pos_ini=[start_pos[0],start_pos[1]+2*size_head]
        if dirc=="down":
            current_pos_ini = [start_pos[0], start_pos[1] - 2*size_head]
        if dirc == "left":
            current_pos_ini = [start_pos[0]+2*size_head, start_pos[1]]
        if dirc == "right":
            current_pos_ini = [start_pos[0] - 2*size_head, start_pos[1]]

        current_checkp=fath_block.get_checkp_no()
        #print("body create",checkp_list)
        block_create_name = "block_{}".format(score)
        new_block_dict[block_create_name] = Block(current_pos_ini, current_checkp,dirc)

def game_over_msg():
    #pygame.mixer.Sound.play(game_over_sound)
    game_over_running=True
    game_over_text = game_over_font.render("Game Over", True, (255, 0, 50))
    game_over_text_rect = game_over_text.get_rect()
    game_over_text_rect.center = (width // 2, depth // 2 + 50)

    score_text = font.render(f"Score :{score}", True, (0, 0, 255))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (width // 2, depth // 2)

    play_again_text = font.render("Press Space to Play Again", True, (90,7,121))
    play_again_text_rect = play_again_text.get_rect()
    play_again_text_rect.center = (width // 2, depth // 2 - 50)



    while game_over_running:
        #pygame.mixer.Sound.play(game_over_msg_sound)
        pygame.draw.rect(screen, (255,255,255), pygame.Rect((width//2)-200, depth//2-75,400, 150))
        screen.blit(game_over_text,game_over_text_rect)

        screen.blit(score_text,score_text_rect)

        screen.blit(play_again_text,play_again_text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                quit()
                game_over_running=False


        #pressed_key_now=pygame.key.get_pressed()
        '''
        if pressed_key_now[pygame.K_SPACE]:
            game_reset()
            game_over_running=False
        '''

'''
def game_reset():
    dir_list = ["left", "right", "up", "down"]
    head_pos = head_gen()  # gives a list with the position of the head
    # head_pos_next=head_pos
    dir_= random.choice(dir_list)  # a random dir is set for initial motion

    # reward configs
    rew_pos = reward_gen()
    score = 0

    # block_num=0
    new_block_dict = {}  # dict to save newly created block
    checkp_list = [[0, 0]]  # checkpoint saving list
    checkp_no = 0  # checkpoint number saving and checkp_no=0 is head_pos
    game_over = False
    running = True
    reset_list[head_pos,dir_,rew_pos,score,new_block_dict,checkp_list,checkp_no,game_over,running]
'''



'''creating a log_file'''
#time_stamp=datetime.datetime.now().timestamp()
'''log_file_name="log_files/log_file_{}".format(time_stamp)'''


clock=pygame.time.Clock()


'''initialisation parameters of the game'''

#dir_list=["left","right","up","down"]
dir_list = ["left", "right", "up", "down"]
head_pos= head_gen() #gives a list with the position of the head
#head_pos_next=head_pos
dir_=random.choice(dir_list) #a random dir is set for initial motion
#reward configs
rew_pos= reward_gen()
#block_num=0
new_block_dict={}   #dict to save newly created block
checkp_list=[[0,0]]      #checkpoint saving list
checkp_no=0        #checkpoint number saving and checkp_no=0 is head_pos
game_over=False
running=True
#background_img=pygame.image.load("backgroundsky.png")
#background_img=pygame.image.load("backgroundsky.jpg")
#background_img=pygame.image.load("background_tree.jpg")
background_img=pygame.image.load("background_6.jpg")
#background_img=pygame.image.load("background_4.png")

#background_img=pygame.image.load("backgroundcheck.png")



snake_speed=3
size_head=10
rew_color = (204,0,204)
rew_size = 7
score=0
fps=100



#game_reset()
try:
    font=pygame.font.Font("Saturday Alright.otf",35)
    game_over_font=pygame.font.Font("Saturday Alright.otf",60)
except:
    load_font=pygame.font.get_default_font()
    font=pygame.font.Font(def_font,35)
    game_over_font=pygame.font.Font(def_font,60)


'''loading musics'''
reward_sound=pygame.mixer.Sound("score_pop.wav")
game_over_msg_sound=pygame.mixer.Sound("game_over_msg.wav")
game_over_sound=pygame.mixer.Sound("game_over.wav")
game_music=pygame.mixer.music.load("gm_music.wav")
pygame.mixer.music.play(-1)

while running:

    screen.fill((0,0,0))
    screen.blit(background_img,(0,0))
    #if score>0:
        #print("block 1_loop big", new_block_dict["block_1"].get_current_pos(), new_block_dict["block_1"].get_next_pos())
    for event in pygame.event.get():
        if event.type== pygame.QUIT:  #to quit the game if X key is pressed
            running=False
            pygame.quit()
            quit()

    #prev_head_pos = head_pos  # to store the head pos before changing it

    if game_over==False:
        head_pos=head_move(head_pos, dir_) #get the position of head according to keyboard inputs

    #setting the boundaries
    head_pos=check_boundary(head_pos)


    #identifying the pressed key and setting motion accordingly
    pressed_key= pygame.key.get_pressed()

    '''
    #pause with space
    if pressed_key[pygame.K_SPACE]:

        paused=True
        pygame.event.clear()
        print(pygame.key.get_pressed())

        while paused:
            print("pause")
            pressed_key_paused=pygame.key.get_pressed()
            if pressed_key_paused[pygame.K_p]:
                paused=False
    '''




    if pressed_key[pygame.K_UP]:
        if dir_ not in ["up", "down"]:
            dir_= "up"
            checkp_no= checkp_no+1
            #head_pos_next=head_move(head_pos, dir_)
            checkp_list.insert(checkp_no,head_pos.copy())

    if pressed_key[pygame.K_DOWN]:
        if dir_ not in ["up", "down"]:
            dir_= "down"
            checkp_no= checkp_no+1
            # head_pos_next=head_move(head_pos, dir_)
            checkp_list.insert(checkp_no, head_pos.copy())

    if pressed_key[pygame.K_RIGHT]:
        if dir_ not in ["left", "right"]:
            dir_= "right"
            checkp_no= checkp_no+1
            # head_pos_next=head_move(head_pos, dir_)
            checkp_list.insert(checkp_no, head_pos.copy())


    if pressed_key[pygame.K_LEFT]:
        if dir_ not in ["left", "right"]:
            dir_= "left"
            checkp_no= checkp_no+1
            # head_pos_next=head_move(head_pos, dir_)
            checkp_list.insert(checkp_no, head_pos.copy())


    pygame.event.clear()

    move_body(score) #function that move body


    #print("dir", dir_)

    #checkp_list[0]=head_pos
    color=(0,25,125)
    size_head = 10
    draw_cicle(head_pos,color,size_head)


    #generating reward object
    rew_head_dist= math.sqrt((rew_pos[0]-head_pos[0])**2+(rew_pos[1]-head_pos[1])**2)

    #increasing length on scoring
    #checkp_list[0] = head_pos.copy()
    if rew_head_dist<10:
        pygame.mixer.Sound.play(reward_sound)
        checkp_no+=1
        checkp_list.insert(checkp_no,head_pos.copy())
        rew_pos = reward_gen()  # gives a list with the position of the reward
        if score>0:
            lapping=True
            while lapping:
                for key in new_block_dict.keys():
                    block_pos_rew=new_block_dict[key].get_current_pos()
                    rew_blk_dist=math.sqrt((block_pos_rew[0]-rew_pos[0])**2+(block_pos_rew[1]-rew_pos[1])**2)
                    if rew_blk_dist< 1.5*size_head:
                        rew_pos=reward_gen()
                    else:
                        lapping=False
        lapping=True
        score+=1        #adds one score per each reward catch
        if score==1:
            create_body_block(score,dir_,checkp_no)
        elif score>1:
            prev_block_name="block_{}".format(score-1)
            prev_block_obj=new_block_dict[prev_block_name]
            create_body_block(score,prev_block_obj.get_direct(),checkp_no)

    #score_text="score :"+str(score)
    text=font.render(f"score :{score}",True,(25,100,80))
    textRect=text.get_rect()
    textRect.center=(50,25)
    screen.blit(text,textRect)



    if pressed_key[pygame.K_ESCAPE]:
        if file_status==1:
            log_file_obj.close()
        running=False
        pygame.quit()
        quit()

    draw_cicle(rew_pos, rew_color, rew_size)
    pygame.display.flip()
    clock.tick(fps)
