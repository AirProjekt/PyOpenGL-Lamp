# coding=utf-8

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math



XMIN = -10.0
XMAX = 10.0
YMIN = -10.0
YMAX = 10.0
M_PI = 3.14159265358979323846
kut = 0.0
alpha = 0.0
betha = 0.0
gama = 0.0

verzija = 0
nn = 16

bijelo = [1.0, 1.0, 1.0, 1.0]
crno = [0.0, 0.0, 0.0, 1.0]
crveno = [1.0, 0.0, 0.0, 1.0]
smedje = [238.0 / 255.0, 154.0 / 255.0, 73.0 / 255.0]
silver = [0.50754,0.50754,0.50754]
zuto = [0.5,0.5,0.0]

def strelica(x, y, z, vx, vy, vz):
    glMaterialfv(GL_FRONT, GL_EMISSION, bijelo)
    glBegin(GL_LINES)
    glVertex3d(x,y,z)
    glVertex3d(x+vx, y+vy, z+vz)
    glEnd()
    glMaterialfv(GL_FRONT, GL_EMISSION, crno)

def normiraj(v):
    d = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    v[0] /= d; v[1] /= d; v[2] /= d
    return v

def vprodukt(v, a0, a1, a2, b0, b1, b2):
    v[0] = a1 * b2 - a2 * b1;
    v[1] = a2 * b0 - a0 * b2;
    v[2] = a0 * b1 - a1 * b0;
    return v

def stozac(r,h,n):
    glBegin(GL_TRIANGLE_FAN)
    glNormal3d(0.0, 0.0, -1.0)
    t = 0.0
    for i in range(n+1):
        glVertex3d(r * math.cos(t), r * math.sin(t), 0.0)
        t += 2.0 * M_PI / n
    glEnd()
    glBegin(GL_TRIANGLE_FAN)
    
    glNormal3d(0.0, 0.0, 1.0) # normala u vrhu stošca u smjeru +z
    glVertex3d(0.0, 0.0, h)
    t = 2.0 * M_PI
    for i in range(n+1):
        glNormal3d(math.cos(t), math.sin(t), 0.0) # normale u xy ravnini - od središta
        glVertex3d(r * math.cos(t), r * math.sin(t), 0.0)
        t -= 2.0 * M_PI / n
    glEnd()

def valjak(r,h,n):
    glBegin(GL_TRIANGLE_FAN)
    glNormal3d(0.0,0.0,-1.0)
    glVertex3d(0.0,0.0,0.0)
    t = 0.0
    for i in range(n+1):
        glVertex3d(r*math.cos(t),r*math.sin(t),0.0)
        t += 2.0 * M_PI / n
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN)
    glNormal3d(0.0,0.0,1.0)
    glVertex3d(0.0,0.0,h)
    t = 0.0
    for i in range(n+1):
        glVertex3d(r*math.cos(t),r*math.sin(t),h)
        t += 2.0 * M_PI / n
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    t = 2.0 * M_PI
    for i in range(n):
        glNormal3d(math.cos(t),math.sin(t),h/r)
        glVertex3d(r*math.cos(t),r*math.sin(t),h)
        glNormal3d(math.cos(t),math.sin(t),0.0)
        glVertex3d(r*math.cos(t),r*math.sin(t),0.0)
        glNormal3d(math.cos(t-2.0*M_PI/n),math.sin(t-2.0*M_PI/n),h/r)
        glVertex3d(r*math.cos(t-2.0*M_PI/n),r*math.sin(t-2.0*M_PI/n),h)
        glNormal3d(math.cos(t-2.0*M_PI/n),math.sin(t-2.0*M_PI/n),0.0)
        glVertex3d(r*math.cos(t-2.0*M_PI/n),r*math.sin(t-2.0*M_PI/n),0.0)
        t -= 2.0 * M_PI / n
    glEnd()
    
def poluvaljak(r,h,n):
    glBegin(GL_TRIANGLE_FAN)
    glNormal3d(0.0,0.0,-1.0)
    glVertex3d(0.0,0.0,0.0)
    t = 0.0
    for i in range(n+1):
        glVertex3d(r*math.cos(t),r*math.sin(t),0.0)
        t += M_PI / n
    glEnd()
    
    glBegin(GL_TRIANGLE_FAN)
    glNormal3d(0.0,0.0,1.0)
    glVertex3d(0.0,0.0,h)
    t = 0.0
    for i in range(n+1):
        glVertex3d(r*math.cos(t),r*math.sin(t),h)
        t += M_PI / n
    glEnd()
    
    glBegin(GL_QUAD_STRIP)
    t = M_PI
    for i in range(n):
        glNormal3d(math.cos(t),math.sin(t),h/r)
        glVertex3d(r*math.cos(t),r*math.sin(t),h)
        glNormal3d(math.cos(t),math.sin(t),0.0)
        glVertex3d(r*math.cos(t),r*math.sin(t),0.0)
        glNormal3d(math.cos(t-M_PI/n),math.sin(t-M_PI/n),h/r)
        glVertex3d(r*math.cos(t-M_PI/n),r*math.sin(t-M_PI/n),h)
        glNormal3d(math.cos(t-M_PI/n),math.sin(t-M_PI/n),0.0)
        glVertex3d(r*math.cos(t-M_PI/n),r*math.sin(t-M_PI/n),0.0)
        t -= M_PI / n
    glEnd()


def kugla(r,n,m):
    fi=0.0
    alfa = 0.0
    i=1
    j=1
  
    glBegin(GL_QUAD_STRIP)
    while fi<2.0*M_PI:
        while alfa<2.0*M_PI:
            glNormal3d(math.sin(fi)*math.cos(alfa), math.sin(fi)*math.sin(alfa), math.cos(fi))
            glVertex3d(r*math.sin(fi)*math.cos(alfa), r*math.sin(fi)*math.sin(alfa), r*math.cos(fi))
            glNormal3d(math.sin(fi+2.0*M_PI/n)*math.cos(alfa), math.sin(fi+2.0*M_PI/n)*math.sin(alfa), math.cos(fi+2.0*M_PI/n))
            glVertex3d(r*math.sin(fi+2.0*M_PI/n)*math.cos(alfa), r*math.sin(fi+2.0*M_PI/n)*math.sin(alfa), r*math.cos(fi+2.0*M_PI/n))
            glNormal3d(math.sin(fi)*math.cos(alfa+2.0*M_PI/m), math.sin(fi)*math.sin(alfa+2.0*M_PI/m), math.cos(fi))
            glVertex3d(r*math.sin(fi)*math.cos(alfa+2.0*M_PI/m), r*math.sin(fi)*math.sin(alfa+2.0*M_PI/m), r*math.cos(fi))
            glNormal3d(math.sin(fi+2.0*M_PI/n)*math.cos(alfa+2.0*M_PI/m), math.sin(fi+2.0*M_PI/n)*math.sin(alfa+2.0*M_PI/m), math.cos(fi+2.0*M_PI/n))
            glVertex3d(r*math.sin(fi+2.0*M_PI/n)*math.cos(alfa+2.0*M_PI/m), r*math.sin(fi+2.0*M_PI/n)*math.sin(alfa+2.0*M_PI/m), r*math.cos(fi+2.0*M_PI/n))
            alfa=alfa+(2.0*M_PI/m)
            j+=1
        fi=fi+(2.0*M_PI/n)
        i+=1    
    glEnd()

def kocka(a):
    glBegin(GL_QUADS);
    # donja ploha je crvena
    glColor3d(1.0, 0.0, 0.0)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(0.0, a, 0.0)
    glVertex3d(a, a, 0.0)
    glVertex3d(a, 0.0, 0.0)

    # gornja ploha je zelena
    glColor3d(0.0, 1.0, 0.0)
    glVertex3d(0.0, 0.0, a)
    glVertex3d(a, 0.0, a)
    glVertex3d(a, a, a)
    glVertex3d(0.0, a, a)
    glEnd()

    # boène plohe
    glBegin(GL_QUAD_STRIP)
    # plava
    glColor3d(0.0, 0.0, 1.0)
    glVertex3d(0.0, 0.0, a)
    glVertex3d(0.0, 0.0, 0.0)
    glVertex3d(a, 0.0, a)
    glVertex3d(a, 0.0, 0.0)

    # žuta
    glColor3d(1.0, 1.0, 0.0)
    glVertex3d(a, a, a)
    glVertex3d(a, a, 0.0)

    # ljubièasta
    glColor3d(1.0, 0.0, 1.0)
    glVertex3d(0.0, a, a)
    glVertex3d(0.0, a, 0.0)

    # plavozelena (cijan)
    glColor3d(0.0, 1.0, 1.0)
    glVertex3d(0.0, 0.0, a)
    glVertex3d(0.0, 0.0, 0.0)
    glEnd()

def svjetlo0():
    pozicija = [0.0, 0.0, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, bijelo)
    glLightfv(GL_LIGHT0, GL_SPECULAR, bijelo)
    glLightfv(GL_LIGHT0, GL_POSITION, pozicija)

def svjetlo1():
    pozicija = [0.0, 0.0, 0.0, 1.0]
    glLightfv(GL_LIGHT1, GL_DIFFUSE, crveno)
    glLightfv(GL_LIGHT1, GL_SPECULAR, crveno)
    glLightfv(GL_LIGHT1, GL_POSITION, pozicija)

 
def iscrtaj():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # kamera
    gluLookAt(20.0, 20.0, 20.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)


    # svjetlo0
    glPushMatrix()
    glTranslated(15.0, 8.0, 15.0)  
    svjetlo0()
    glMaterialfv(GL_FRONT, GL_EMISSION, bijelo)
    kocka(0.5)
    glMaterialfv(GL_FRONT, GL_EMISSION, crno)
    glPopMatrix()


    glPushMatrix()
    glRotated(-alpha,1.0,0.0,0.0)
    glRotated(-betha,1.0,0.0,0.0)
    glRotated(-gama,1.0,0.0,0.0)
    glTranslated(-6.5, 0.0, 4.0)
    svjetlo1()
    glMaterialfv(GL_FRONT, GL_EMISSION, crveno)
    kocka(0.5)
    glMaterialfv(GL_FRONT, GL_EMISSION, crno)
    glPopMatrix()
    
    glMaterialfv(GL_FRONT, GL_DIFFUSE, zuto);
    glMaterialfv(GL_FRONT, GL_SPECULAR, bijelo);
    glMaterialf(GL_FRONT, GL_SHININESS, 20.0);
    
    kugla(25, 5, 5)

    glMaterialfv(GL_FRONT, GL_DIFFUSE, silver);
    glMaterialfv(GL_FRONT, GL_SPECULAR, bijelo);
    glMaterialf(GL_FRONT, GL_SHININESS, 20.0);

    glTranslated(0.0,0.0,-6.0)
    valjak(5,1,500)
    glTranslated(0.0,0.0,1.0)
    valjak(2, 0.5, 500)
    glTranslated(0.0,0.0,0.5)
    glRotated(90.0,1.0,0.0,0.0)
    glRotated(120.0,0.0,1.0,0.0)
    glTranslated(0.4,0.8,0.0)
    poluvaljak(1, 2.5, 500)
    glPushMatrix()
    glRotated(-90.0,1.0,0.0,0.0)
    glRotated(-30.0,0.0,1.0,0.0)
    glTranslated(0.0,-0.3,0.0)
    glRotated(gama,0.0,1.0,0.0)
    valjak(0.4,7,500)
    glTranslated(0.0,-1.8,0.0)
    valjak(0.4, 7, 500)
    glPopMatrix()
    glRotated(-gama,0.0,0.0,1.0)
    glTranslated(-3.5,6.0,0.0)
    valjak(0.5, 2.5, 500)
    glPushMatrix()
    glRotated(90.0,0.0,1.0,0.0)
    glRotated(-30.0,1.0,0.0,0.0)
    glTranslated(-0.2,0.0,0.0)
    glRotated(betha,1.0,0.0,0.0)
    valjak(0.4, 7, 500)
    glTranslated(-1.8,0.0,0.0)
    valjak(0.4, 7, 500)
    glPopMatrix()
    glRotated(-betha,0.0,0.0,1.0) 
    glTranslated(6.3,3.7,0.0)
    valjak(0.5, 2.5, 500)
    glRotated(90.0,0.0,1.0,0.0)
    glRotated(-30.0,1.0,0.0,0.0)
    glTranslated(-1.3,0.0,0.0)
    glRotated(alpha,1.0,0.0,0.0)
    valjak(0.4, 1.3, 500)
    glRotated(-90.0,1.0,0.0,0.0)
    glTranslated(0.0,-2.0,0.0)
    valjak(1.0, 2.5, 500)
    glTranslated(0.0,0.0,-1.2)
    stozac(2.0,3.0 , 500)
    
    glutSwapBuffers()

def skaliraj(Width, Height):
    xrange = XMAX - XMIN
    yrange = Height * xrange / Width

    glViewport(0, 0, Width, Height)		
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(XMIN, XMAX, -yrange / 2.0, yrange / 2.0, 20.0, 50.0)

def tipka(*args):
    global alpha
    global betha
    global gama
    if args[0] == 'q':
        sys.exit()
    elif args[0] == 's':
        glShadeModel(GL_SMOOTH)
    elif args[0] == 'f':
        glShadeModel(GL_FLAT)
    elif args[0] == 'B':
        glCullFace(GL_BACK)
    elif args[0] == 'b':
        glCullFace(GL_FRONT)
    elif args[0] == 'C':
        glEnable(GL_CULL_FACE)
    elif args[0] == 'c':
        glDisable(GL_CULL_FACE)
    elif args[0] == 'D':
        glEnable(GL_DEPTH_TEST)
    elif args[0] == 'd':
        glDisable(GL_DEPTH_TEST)
    elif args[0] == 'P':
        glEnable(GL_LIGHT0)
    elif args[0] == 'p':
        glDisable(GL_LIGHT0)
    elif args[0] == 'O':
        glEnable(GL_LIGHT1)
    elif args[0] == 'o':
        glDisable(GL_LIGHT1)
    elif args[0] == '1':
        alpha += 1
        if alpha>20:
            alpha = 20
    elif args[0] == '2':
        alpha -= 1
        if alpha<-20:
            alpha = -20
    elif args[0] == '3':
        betha += 1
        if betha>20:
            betha = 20
    elif args[0] == '4':
        betha -= 1
        if betha<-20:
            betha = -20
    elif args[0] == '5':
        gama += 1
        if gama>20:
            gama = 20
    elif args[0] == '6':
        gama -= 1
        if gama<-20:
            gama = -20
    

def rotiraj():
    global kut
    kut += -0.2
    glutPostRedisplay()

def main():
    glutInit(())
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    
    glutInitWindowSize(800, 600)
    glutInitWindowPosition(0, 0)
    
    glutCreateWindow("Lampa")
    
    glShadeModel(GL_FLAT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
  
    glutDisplayFunc(iscrtaj)
    glutReshapeFunc(skaliraj)
    glutKeyboardFunc(tipka)
    glutIdleFunc(rotiraj)
    glutMainLoop()

main()
    	

