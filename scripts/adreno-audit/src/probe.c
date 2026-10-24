#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/sync_file.h>
#include <sys/mman.h>
#include <sys/utsname.h>
#include <poll.h>
#include <android/hardware_buffer.h>
#include <android/native_window_jni.h>
#include <time.h>
#include <EGL/egl.h>
#include <EGL/eglext.h>
#include <GLES3/gl31.h>
#include <GLES2/gl2ext.h>
#include <vulkan/vulkan.h>
#define __user
#include "msm_kgsl.h"
#ifdef APP_PROBE
#include <jni.h>
#endif
static FILE *out;
static unsigned failures, passes;
#define INFO(...)                                                                                  \
    do {                                                                                           \
        fprintf(out, "INFO\t");                                                                    \
        fprintf(out, __VA_ARGS__);                                                                 \
        fputc('\n', out);                                                                          \
        fflush(out);                                                                               \
    } while (0)
#define CHECK(name, cond)                                                                          \
    do {                                                                                           \
        int audit_condition_passed = !!(cond);                                                     \
        fprintf(out, "%s\t%s\n", audit_condition_passed ? "PASS" : "FAIL", name);                  \
        fflush(out);                                                                               \
        if (audit_condition_passed)                                                                \
            passes++;                                                                              \
        else                                                                                       \
            failures++;                                                                            \
    } while (0)
static GLuint shader(GLenum type, const char *src) {
    GLuint s = glCreateShader(type);
    glShaderSource(s, 1, &src, NULL);
    glCompileShader(s);
    GLint ok = 0;
    glGetShaderiv(s, GL_COMPILE_STATUS, &ok);
    if (!ok) {
        char b[2048];
        glGetShaderInfoLog(s, sizeof(b), NULL, b);
        INFO("shader error: %s", b);
        glDeleteShader(s);
        return 0;
    }
    return s;
}
static GLuint program(const char *v, const char *f) {
    GLuint vs = shader(GL_VERTEX_SHADER, v), fs = shader(GL_FRAGMENT_SHADER, f);
    if (!vs || !fs) {
        if (vs)
            glDeleteShader(vs);
        if (fs)
            glDeleteShader(fs);
        return 0;
    }
    GLuint p = glCreateProgram();
    glAttachShader(p, vs);
    glAttachShader(p, fs);
    glBindAttribLocation(p, 0, "pos");
    glLinkProgram(p);
    glDeleteShader(vs);
    glDeleteShader(fs);
    GLint ok = 0;
    glGetProgramiv(p, GL_LINK_STATUS, &ok);
    if (!ok) {
        glDeleteProgram(p);
        return 0;
    }
    return p;
}
static void kgsl(void) {
    int fd = open("/dev/kgsl-3d0", O_RDWR | O_CLOEXEC);
    CHECK("kgsl.open", fd >= 0);
    if (fd < 0) {
        INFO("kgsl errno=%d", errno);
        return;
    }
    struct kgsl_devinfo info = {0};
    struct kgsl_device_getproperty prop = {
        .type = KGSL_PROP_DEVICE_INFO, .value = &info, .sizebytes = sizeof(info)};
    int rc = ioctl(fd, IOCTL_KGSL_DEVICE_GETPROPERTY, &prop);
    CHECK("kgsl.device_info", rc == 0 && (info.chip_id >> 16) == 0x605 && info.gmem_sizebytes > 0 &&
                                  info.mmu_enabled != 0);
    INFO("gpu_id=%u chip_id=0x%x mmu=%u gmem=%zu", info.gpu_id, info.chip_id, info.mmu_enabled,
         info.gmem_sizebytes);
    int good = 1;
    for (int i = 0; i < 100; i++) {
        struct kgsl_gpumem_alloc_id a = {.size = 65536};
        if (ioctl(fd, IOCTL_KGSL_GPUMEM_ALLOC_ID, &a)) {
            good = 0;
            INFO("kgsl alloc errno=%d iteration=%d", errno, i);
            break;
        }
        struct kgsl_gpumem_get_info q = {.id = a.id};
        if (ioctl(fd, IOCTL_KGSL_GPUMEM_GET_INFO, &q) || q.size < 65536)
            good = 0;
        void *m =
            mmap(NULL, a.mmapsize, PROT_READ | PROT_WRITE, MAP_SHARED, fd, (off_t)a.id * 4096);
        if (m == MAP_FAILED) {
            good = 0;
            INFO("kgsl mmap errno=%d size=%zu", errno, a.mmapsize);
        } else {
            memset(m, 0x5a, 65536);
            if (((unsigned char *)m)[65535] != 0x5a)
                good = 0;
            munmap(m, a.mmapsize);
        }
        struct kgsl_gpumem_free_id f = {.id = a.id};
        if (ioctl(fd, IOCTL_KGSL_GPUMEM_FREE_ID, &f))
            good = 0;
        if (!good)
            break;
    }
    CHECK("kgsl.alloc_query_mmap_free_100", good);
    struct kgsl_gpuobj_alloc obj = {.size = 65536,
                                    .flags = (KGSL_CACHEMODE_WRITEBACK << KGSL_CACHEMODE_SHIFT)};
    rc = ioctl(fd, IOCTL_KGSL_GPUOBJ_ALLOC, &obj);
    CHECK("kgsl.gpuobj_alloc", rc == 0);
    if (!rc) {
        struct kgsl_gpuobj_info oi = {.id = obj.id};
        rc = ioctl(fd, IOCTL_KGSL_GPUOBJ_INFO, &oi);
        CHECK("kgsl.gpuobj_info", rc == 0 && oi.size >= 65536);
        void *ptr =
            mmap(NULL, obj.mmapsize, PROT_READ | PROT_WRITE, MAP_SHARED, fd, (off_t)obj.id * 4096);
        CHECK("kgsl.gpuobj_mmap", ptr != MAP_FAILED);
        if (ptr != MAP_FAILED) {
            memset(ptr, 0x3c, 65536);
            struct kgsl_gpuobj_sync_obj so = {
                .id = obj.id, .offset = 0, .length = 65536, .op = KGSL_GPUMEM_CACHE_FLUSH};
            struct kgsl_gpuobj_sync sync = {
                .objs = (uintptr_t)&so, .obj_len = sizeof(so), .count = 1};
            CHECK("kgsl.gpuobj_cache_sync", ioctl(fd, IOCTL_KGSL_GPUOBJ_SYNC, &sync) == 0);
            munmap(ptr, obj.mmapsize);
        }
        struct kgsl_gpuobj_free fr = {.id = obj.id};
        CHECK("kgsl.gpuobj_free", ioctl(fd, IOCTL_KGSL_GPUOBJ_FREE, &fr) == 0);
    }
    struct kgsl_timeline_create tc = {.seqno = 1};
    rc = ioctl(fd, IOCTL_KGSL_TIMELINE_CREATE, &tc);
    CHECK("kgsl.timeline_create", rc == 0);
    if (!rc) {
        struct kgsl_timeline_val tv = {.timeline = tc.id};
        rc = ioctl(fd, IOCTL_KGSL_TIMELINE_QUERY, &tv);
        CHECK("kgsl.timeline_query", rc == 0 && tv.seqno == 1);
        struct kgsl_timeline_fence_get tf = {.timeline = tc.id, .seqno = 2, .handle = -1};
        rc = ioctl(fd, IOCTL_KGSL_TIMELINE_FENCE_GET, &tf);
        CHECK("kgsl.timeline_fence_get", rc == 0 && tf.handle >= 0);
        struct kgsl_timeline_fence_get second = {.timeline = tc.id, .seqno = 3, .handle = -1};
        int second_rc = ioctl(fd, IOCTL_KGSL_TIMELINE_FENCE_GET, &second);
        CHECK("kgsl.timeline_second_fence", second_rc == 0 && second.handle >= 0);
        struct sync_merge_data merge = {.fd2 = second.handle, .fence = -1};
        strcpy(merge.name, "codex-gpu-audit");
        int merged = -1;
        if (!rc && tf.handle >= 0 && !second_rc && second.handle >= 0) {
            int merge_rc = ioctl(tf.handle, SYNC_IOC_MERGE, &merge);
            CHECK("sync_file.merge", merge_rc == 0 && merge.fence >= 0);
            if (!merge_rc) {
                merged = merge.fence;
                struct pollfd pending = {.fd = merged, .events = POLLIN};
                CHECK("sync_file.unsignaled_poll", poll(&pending, 1, 0) == 0);
            }
        }
        tv.seqno = 3;
        struct kgsl_timeline_signal ts = {
            .timelines = (uintptr_t)&tv, .count = 1, .timelines_size = sizeof(tv)};
        CHECK("kgsl.timeline_signal", ioctl(fd, IOCTL_KGSL_TIMELINE_SIGNAL, &ts) == 0);
        if (!rc && tf.handle >= 0) {
            struct pollfd f = {.fd = tf.handle, .events = POLLIN};
            CHECK("kgsl.timeline_fence_poll", poll(&f, 1, 2000) == 1 && (f.revents & POLLIN));
            close(tf.handle);
        }
        if (merged >= 0) {
            struct pollfd ready = {.fd = merged, .events = POLLIN};
            CHECK("sync_file.merged_fence_poll",
                  poll(&ready, 1, 2000) == 1 && (ready.revents & POLLIN));
            close(merged);
        }
        if (second.handle >= 0)
            close(second.handle);
        struct kgsl_timeline_wait tw = {.tv_sec = 1,
                                        .timelines = (uintptr_t)&tv,
                                        .count = 1,
                                        .timelines_size = sizeof(tv),
                                        .flags = KGSL_TIMELINE_WAIT_ALL};
        CHECK("kgsl.timeline_wait", ioctl(fd, IOCTL_KGSL_TIMELINE_WAIT, &tw) == 0);
        CHECK("kgsl.timeline_destroy", ioctl(fd, IOCTL_KGSL_TIMELINE_DESTROY, &tc.id) == 0);
    }

    if (getenv("GPU_AUDIT_SPARSE_REGRESSION")) {
        struct utsname un;
        uname(&un);
        if (!strstr(un.release, "gb8fc2fc50a5c")) {
            INFO("SKIP sparse regression: unverified kernel; mapping-index fix must be confirmed "
                 "before use");
        } else {
            struct kgsl_sparse_phys_alloc pa = {.size = 65536, .pagesize = 65536};
            int sr = ioctl(fd, IOCTL_KGSL_SPARSE_PHYS_ALLOC, &pa);
            if (sr && (errno == EOPNOTSUPP || errno == ENOTSUP || errno == 524))
                INFO("SKIP sparse regression: device does not enable sparse allocations");
            else {
                CHECK("kgsl.sparse_phys_alloc_64k", sr == 0);
                if (!sr) {
                    struct kgsl_sparse_virt_alloc va = {.size = 262144, .pagesize = 65536};
                    sr = ioctl(fd, IOCTL_KGSL_SPARSE_VIRT_ALLOC, &va);
                    CHECK("kgsl.sparse_virt_alloc_256k", sr == 0);
                    if (!sr) {
                        struct kgsl_sparse_binding_object bo = {
                            .size = 262144,
                            .flags = KGSL_SPARSE_BIND | KGSL_SPARSE_BIND_MULTIPLE_TO_PHYS,
                            .id = pa.id};
                        struct kgsl_sparse_bind bind = {
                            .list = (uintptr_t)&bo, .id = va.id, .size = sizeof(bo), .count = 1};
                        sr = ioctl(fd, IOCTL_KGSL_SPARSE_BIND, &bind);
                        CHECK("kgsl.sparse_repeat_64k_across_256k", sr == 0);
                        if (!sr) {
                            bo.flags = KGSL_SPARSE_UNBIND;
                            CHECK("kgsl.sparse_unbind",
                                  ioctl(fd, IOCTL_KGSL_SPARSE_BIND, &bind) == 0);
                        }
                        struct kgsl_sparse_virt_free vf = {.id = va.id};
                        CHECK("kgsl.sparse_virt_free",
                              ioctl(fd, IOCTL_KGSL_SPARSE_VIRT_FREE, &vf) == 0);
                    }
                    struct kgsl_sparse_phys_free pf = {.id = pa.id};
                    CHECK("kgsl.sparse_phys_free",
                          ioctl(fd, IOCTL_KGSL_SPARSE_PHYS_FREE, &pf) == 0);
                }
            }
        }
    }
    struct kgsl_drawctxt_create c = {.flags = KGSL_CONTEXT_PREAMBLE | KGSL_CONTEXT_NO_GMEM_ALLOC};
    rc = ioctl(fd, IOCTL_KGSL_DRAWCTXT_CREATE, &c);
    CHECK("kgsl.context_create", rc == 0);
    if (!rc) {
        struct kgsl_drawctxt_destroy d = {.drawctxt_id = c.drawctxt_id};
        CHECK("kgsl.context_destroy", ioctl(fd, IOCTL_KGSL_DRAWCTXT_DESTROY, &d) == 0);
    }
    close(fd);
}
static void gles(int version) {
    EGLDisplay d = eglGetDisplay(EGL_DEFAULT_DISPLAY);
    EGLint major = 0, minor = 0;
    int ok = eglInitialize(d, &major, &minor);
    CHECK(version == 2 ? "egl.initialize.es2" : "egl.initialize.es3", ok);
    if (!ok)
        return;
    INFO("EGL %d.%d vendor=%s extensions=%s", major, minor, eglQueryString(d, EGL_VENDOR),
         eglQueryString(d, EGL_EXTENSIONS));
    EGLint cfgattr[] = {EGL_SURFACE_TYPE,
                        EGL_PBUFFER_BIT,
                        EGL_RENDERABLE_TYPE,
                        version == 2 ? EGL_OPENGL_ES2_BIT : EGL_OPENGL_ES3_BIT_KHR,
                        EGL_RED_SIZE,
                        8,
                        EGL_GREEN_SIZE,
                        8,
                        EGL_BLUE_SIZE,
                        8,
                        EGL_ALPHA_SIZE,
                        8,
                        EGL_NONE};
    EGLConfig cfg;
    EGLint count = 0;
    ok = eglChooseConfig(d, cfgattr, &cfg, 1, &count) && count;
    CHECK("egl.config", ok);
    if (!ok) {
        eglTerminate(d);
        return;
    }
    EGLint pb[] = {EGL_WIDTH, 64, EGL_HEIGHT, 64, EGL_NONE},
           ca[] = {EGL_CONTEXT_CLIENT_VERSION, version, EGL_NONE};
    EGLSurface surf = eglCreatePbufferSurface(d, cfg, pb);
    EGLContext ctx = eglCreateContext(d, cfg, EGL_NO_CONTEXT, ca);
    ok = surf != EGL_NO_SURFACE && ctx != EGL_NO_CONTEXT && eglMakeCurrent(d, surf, surf, ctx);
    CHECK("egl.context_pbuffer_current", ok);
    if (!ok)
        goto done;
    INFO("GL requested=%d renderer=%s version=%s glsl=%s", version, glGetString(GL_RENDERER),
         glGetString(GL_VERSION), glGetString(GL_SHADING_LANGUAGE_VERSION));
    if (version == 3) {
        GLint n = 0;
        glGetIntegerv(GL_NUM_EXTENSIONS, &n);
        for (int i = 0; i < n; i++)
            INFO("GL_EXT %s", glGetStringi(GL_EXTENSIONS, i));
    }
    glViewport(0, 0, 64, 64);
    glClearColor(1, 0, 0, 1);
    glClear(GL_COLOR_BUFFER_BIT);
    unsigned char pixel[4] = {0};
    glReadPixels(32, 32, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, pixel);
    CHECK("gles.clear_readback", pixel[0] == 255 && pixel[1] == 0 && pixel[2] == 0 &&
                                     pixel[3] == 255 && glGetError() == GL_NO_ERROR);
    const char *vs = "attribute vec2 pos;void main(){gl_Position=vec4(pos,0.0,1.0);}";
    const char *fs = "precision mediump float;void main(){gl_FragColor=vec4(0.0,1.0,0.0,1.0);}";
    GLuint pr = program(vs, fs);
    CHECK("gles.shader_compile_link", pr != 0);
    if (pr) {
        GLuint buf;
        float verts[] = {-1, -1, 3, -1, -1, 3};
        glGenBuffers(1, &buf);
        glBindBuffer(GL_ARRAY_BUFFER, buf);
        glBufferData(GL_ARRAY_BUFFER, sizeof(verts), verts, GL_STATIC_DRAW);
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0);
        glEnableVertexAttribArray(0);
        glUseProgram(pr);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        glReadPixels(32, 32, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, pixel);
        CHECK("gles.draw_readback",
              pixel[0] == 0 && pixel[1] == 255 && pixel[2] == 0 && glGetError() == GL_NO_ERROR);
        glDisableVertexAttribArray(0);
        glDeleteBuffers(1, &buf);
        glDeleteProgram(pr);
    }
    if (version == 3) {
        const char *cs =
            "#version 310 es\nlayout(local_size_x=64) in;layout(std430,binding=0) buffer Data{uint "
            "values[];};void main(){uint i=gl_GlobalInvocationID.x;values[i]=i*3u+7u;}";
        GLuint s = shader(GL_COMPUTE_SHADER, cs), p = glCreateProgram();
        if (s)
            glAttachShader(p, s);
        glLinkProgram(p);
        GLint linked = 0;
        glGetProgramiv(p, GL_LINK_STATUS, &linked);
        CHECK("gles.compute_compile_link", linked);
        if (linked) {
            GLuint b;
            glGenBuffers(1, &b);
            glBindBuffer(GL_SHADER_STORAGE_BUFFER, b);
            glBufferData(GL_SHADER_STORAGE_BUFFER, 1024, NULL, GL_DYNAMIC_READ);
            glBindBufferBase(GL_SHADER_STORAGE_BUFFER, 0, b);
            glUseProgram(p);
            glDispatchCompute(4, 1, 1);
            glMemoryBarrier(GL_BUFFER_UPDATE_BARRIER_BIT);
            glFinish();
            uint32_t *v = glMapBufferRange(GL_SHADER_STORAGE_BUFFER, 0, 1024, GL_MAP_READ_BIT);
            int valid = v != NULL;
            if (v) {
                for (unsigned i = 0; i < 256; i++)
                    if (v[i] != i * 3 + 7)
                        valid = 0;
                glUnmapBuffer(GL_SHADER_STORAGE_BUFFER);
            }
            CHECK("gles.compute_dispatch_barrier_readback", valid && glGetError() == GL_NO_ERROR);
            glDeleteBuffers(1, &b);
        }
        if (s)
            glDeleteShader(s);
        glDeleteProgram(p);
        GLsync sy = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
        GLenum wait = glClientWaitSync(sy, GL_SYNC_FLUSH_COMMANDS_BIT, 2000000000ULL);
        CHECK("gles.fence_wait", wait == GL_ALREADY_SIGNALED || wait == GL_CONDITION_SATISFIED);
        if (sy)
            glDeleteSync(sy);
    }
    const char *ext = eglQueryString(d, EGL_EXTENSIONS);
    if (ext && strstr(ext, "EGL_ANDROID_native_fence_sync")) {
        PFNEGLCREATESYNCKHRPROC create = (void *)eglGetProcAddress("eglCreateSyncKHR");
        PFNEGLDESTROYSYNCKHRPROC destroy = (void *)eglGetProcAddress("eglDestroySyncKHR");
        PFNEGLDUPNATIVEFENCEFDANDROIDPROC dupfd =
            (void *)eglGetProcAddress("eglDupNativeFenceFDANDROID");
        if (create && destroy && dupfd) {
            EGLSyncKHR sy = create(d, EGL_SYNC_NATIVE_FENCE_ANDROID, NULL);
            glFlush();
            int fd = dupfd(d, sy);
            struct pollfd pfd = {.fd = fd, .events = POLLIN};
            int ready = fd >= 0 ? poll(&pfd, 1, 2000) : -1;
            CHECK("egl.native_fence_fd_poll", ready == 1 && (pfd.revents & POLLIN));
            if (fd >= 0)
                close(fd);
            destroy(d, sy);
        } else
            CHECK("egl.native_fence_entrypoints", 0);
    }
    if (version == 3) {
        AHardwareBuffer_Desc desc = {.width = 16,
                                     .height = 16,
                                     .layers = 1,
                                     .format = AHARDWAREBUFFER_FORMAT_R8G8B8A8_UNORM,
                                     .usage = AHARDWAREBUFFER_USAGE_CPU_READ_OFTEN |
                                              AHARDWAREBUFFER_USAGE_CPU_WRITE_OFTEN |
                                              AHARDWAREBUFFER_USAGE_GPU_SAMPLED_IMAGE |
                                              AHARDWAREBUFFER_USAGE_GPU_COLOR_OUTPUT};
        AHardwareBuffer *ahb = NULL;
        int rc = AHardwareBuffer_allocate(&desc, &ahb);
        CHECK("ahb.allocate_rgba", rc == 0 && ahb);
        if (!rc && ahb) {
            PFNEGLGETNATIVECLIENTBUFFERANDROIDPROC get =
                (void *)eglGetProcAddress("eglGetNativeClientBufferANDROID");
            PFNEGLCREATEIMAGEKHRPROC create = (void *)eglGetProcAddress("eglCreateImageKHR");
            PFNEGLDESTROYIMAGEKHRPROC destroy = (void *)eglGetProcAddress("eglDestroyImageKHR");
            PFNGLEGLIMAGETARGETTEXTURE2DOESPROC target =
                (void *)eglGetProcAddress("glEGLImageTargetTexture2DOES");
            CHECK("ahb.egl_entrypoints", get && create && destroy && target);
            if (get && create && destroy && target) {
                EGLClientBuffer client = get(ahb);
                EGLImageKHR image =
                    create(d, EGL_NO_CONTEXT, EGL_NATIVE_BUFFER_ANDROID, client, NULL);
                CHECK("ahb.egl_image_import", image != EGL_NO_IMAGE_KHR);
                if (image != EGL_NO_IMAGE_KHR) {
                    GLuint tex, fbo;
                    glGenTextures(1, &tex);
                    glBindTexture(GL_TEXTURE_2D, tex);
                    target(GL_TEXTURE_2D, image);
                    glGenFramebuffers(1, &fbo);
                    glBindFramebuffer(GL_FRAMEBUFFER, fbo);
                    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, tex,
                                           0);
                    int complete =
                        glCheckFramebufferStatus(GL_FRAMEBUFFER) == GL_FRAMEBUFFER_COMPLETE;
                    CHECK("ahb.framebuffer_complete", complete);
                    if (complete) {
                        glClearColor(0, 0, 1, 1);
                        glClear(GL_COLOR_BUFFER_BIT);
                        glFinish();
                        void *cpu = NULL;
                        rc = AHardwareBuffer_lock(ahb, AHARDWAREBUFFER_USAGE_CPU_READ_OFTEN, -1,
                                                  NULL, &cpu);
                        int valid = rc == 0 && cpu;
                        if (valid) {
                            unsigned char *v = cpu;
                            valid = v[0] == 0 && v[1] == 0 && v[2] == 255 && v[3] == 255;
                            AHardwareBuffer_unlock(ahb, NULL);
                        }
                        CHECK("ahb.gpu_write_cpu_readback", valid);
                    }
                    glBindFramebuffer(GL_FRAMEBUFFER, 0);
                    glDeleteFramebuffers(1, &fbo);
                    glDeleteTextures(1, &tex);
                    destroy(d, image);
                }
            }
            AHardwareBuffer_release(ahb);
        }
    }
    glFinish();
    CHECK("gles.final_error", glGetError() == GL_NO_ERROR);
done:
    eglMakeCurrent(d, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT);
    if (ctx != EGL_NO_CONTEXT)
        eglDestroyContext(d, ctx);
    if (surf != EGL_NO_SURFACE)
        eglDestroySurface(d, surf);
    eglTerminate(d);
    eglReleaseThread();
}
static void vulkan(void) {
    VkApplicationInfo ai = {.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO,
                            .pApplicationName = "AliothAudit",
                            .apiVersion = VK_API_VERSION_1_0};
    VkInstanceCreateInfo ci = {.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
                               .pApplicationInfo = &ai};
    VkInstance instance = VK_NULL_HANDLE;
    VkResult rc = vkCreateInstance(&ci, NULL, &instance);
    CHECK("vk.create_instance", rc == VK_SUCCESS);
    if (rc)
        return;
    uint32_t count = 0;
    rc = vkEnumeratePhysicalDevices(instance, &count, NULL);
    CHECK("vk.enumerate_devices", rc == VK_SUCCESS && count > 0);
    if (rc || !count) {
        vkDestroyInstance(instance, NULL);
        return;
    }
    VkPhysicalDevice *devs = calloc(count, sizeof(*devs));
    vkEnumeratePhysicalDevices(instance, &count, devs);
    VkPhysicalDevice phy = devs[0];
    free(devs);
    VkPhysicalDeviceProperties props;
    vkGetPhysicalDeviceProperties(phy, &props);
    INFO("VK device=%s api=%u.%u.%u driver=0x%x vendor=0x%x", props.deviceName,
         VK_VERSION_MAJOR(props.apiVersion), VK_VERSION_MINOR(props.apiVersion),
         VK_VERSION_PATCH(props.apiVersion), props.driverVersion, props.vendorID);
    uint32_t ec = 0;
    vkEnumerateDeviceExtensionProperties(phy, NULL, &ec, NULL);
    VkExtensionProperties *eps = calloc(ec, sizeof(*eps));
    vkEnumerateDeviceExtensionProperties(phy, NULL, &ec, eps);
    for (unsigned i = 0; i < ec; i++)
        INFO("VK_EXT %s %u", eps[i].extensionName, eps[i].specVersion);
    free(eps);
    uint32_t qc = 0;
    vkGetPhysicalDeviceQueueFamilyProperties(phy, &qc, NULL);
    VkQueueFamilyProperties *qs = calloc(qc, sizeof(*qs));
    vkGetPhysicalDeviceQueueFamilyProperties(phy, &qc, qs);
    uint32_t family = UINT32_MAX;
    for (unsigned i = 0; i < qc; i++)
        if (qs[i].queueFlags & VK_QUEUE_GRAPHICS_BIT) {
            family = i;
            break;
        }
    free(qs);
    CHECK("vk.graphics_queue", family != UINT32_MAX);
    if (family == UINT32_MAX) {
        vkDestroyInstance(instance, NULL);
        return;
    }
    float priority = 1;
    VkDeviceQueueCreateInfo qi = {.sType = VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
                                  .queueFamilyIndex = family,
                                  .queueCount = 1,
                                  .pQueuePriorities = &priority};
    VkDeviceCreateInfo di = {.sType = VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
                             .queueCreateInfoCount = 1,
                             .pQueueCreateInfos = &qi};
    VkDevice dev = VK_NULL_HANDLE;
    rc = vkCreateDevice(phy, &di, NULL, &dev);
    CHECK("vk.create_device", rc == VK_SUCCESS);
    if (rc) {
        vkDestroyInstance(instance, NULL);
        return;
    }
    VkQueue queue;
    vkGetDeviceQueue(dev, family, 0, &queue);
    VkBuffer buf = VK_NULL_HANDLE;
    VkDeviceMemory mem = VK_NULL_HANDLE;
    VkCommandPool pool = VK_NULL_HANDLE;
    VkFence fence = VK_NULL_HANDLE;
    VkBufferCreateInfo bi = {.sType = VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO,
                             .size = 4096,
                             .usage = VK_BUFFER_USAGE_TRANSFER_DST_BIT |
                                      VK_BUFFER_USAGE_TRANSFER_SRC_BIT,
                             .sharingMode = VK_SHARING_MODE_EXCLUSIVE};
    rc = vkCreateBuffer(dev, &bi, NULL, &buf);
    CHECK("vk.create_buffer", rc == VK_SUCCESS);
    if (rc)
        goto done;
    VkMemoryRequirements mr;
    vkGetBufferMemoryRequirements(dev, buf, &mr);
    VkPhysicalDeviceMemoryProperties mp;
    vkGetPhysicalDeviceMemoryProperties(phy, &mp);
    uint32_t type = UINT32_MAX;
    for (unsigned i = 0; i < mp.memoryTypeCount; i++)
        if ((mr.memoryTypeBits & (1u << i)) &&
            (mp.memoryTypes[i].propertyFlags &
             (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)) ==
                (VK_MEMORY_PROPERTY_HOST_VISIBLE_BIT | VK_MEMORY_PROPERTY_HOST_COHERENT_BIT)) {
            type = i;
            break;
        }
    CHECK("vk.host_coherent_memory_type", type != UINT32_MAX);
    if (type == UINT32_MAX)
        goto done;
    VkMemoryAllocateInfo ma = {.sType = VK_STRUCTURE_TYPE_MEMORY_ALLOCATE_INFO,
                               .allocationSize = mr.size,
                               .memoryTypeIndex = type};
    rc = vkAllocateMemory(dev, &ma, NULL, &mem);
    CHECK("vk.allocate_memory", rc == VK_SUCCESS);
    if (rc)
        goto done;
    rc = vkBindBufferMemory(dev, buf, mem, 0);
    CHECK("vk.bind_memory", rc == VK_SUCCESS);
    if (rc)
        goto done;
    VkCommandPoolCreateInfo pi = {.sType = VK_STRUCTURE_TYPE_COMMAND_POOL_CREATE_INFO,
                                  .queueFamilyIndex = family};
    rc = vkCreateCommandPool(dev, &pi, NULL, &pool);
    CHECK("vk.create_command_pool", rc == VK_SUCCESS);
    if (rc)
        goto done;
    VkCommandBuffer cb;
    VkCommandBufferAllocateInfo ba = {.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_ALLOCATE_INFO,
                                      .commandPool = pool,
                                      .level = VK_COMMAND_BUFFER_LEVEL_PRIMARY,
                                      .commandBufferCount = 1};
    rc = vkAllocateCommandBuffers(dev, &ba, &cb);
    CHECK("vk.allocate_command_buffer", rc == VK_SUCCESS);
    if (rc)
        goto done;
    VkCommandBufferBeginInfo begin = {.sType = VK_STRUCTURE_TYPE_COMMAND_BUFFER_BEGIN_INFO};
    rc = vkBeginCommandBuffer(cb, &begin);
    CHECK("vk.begin_command_buffer", rc == VK_SUCCESS);
    if (rc)
        goto done;
    vkCmdFillBuffer(cb, buf, 0, 4096, 0xa5c35a7e);
    VkBufferMemoryBarrier barrier = {.sType = VK_STRUCTURE_TYPE_BUFFER_MEMORY_BARRIER,
                                     .srcAccessMask = VK_ACCESS_TRANSFER_WRITE_BIT,
                                     .dstAccessMask = VK_ACCESS_HOST_READ_BIT,
                                     .srcQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED,
                                     .dstQueueFamilyIndex = VK_QUEUE_FAMILY_IGNORED,
                                     .buffer = buf,
                                     .offset = 0,
                                     .size = VK_WHOLE_SIZE};
    vkCmdPipelineBarrier(cb, VK_PIPELINE_STAGE_TRANSFER_BIT, VK_PIPELINE_STAGE_HOST_BIT, 0, 0, NULL,
                         1, &barrier, 0, NULL);
    rc = vkEndCommandBuffer(cb);
    CHECK("vk.end_command_buffer", rc == VK_SUCCESS);
    if (rc)
        goto done;
    VkFenceCreateInfo fi = {.sType = VK_STRUCTURE_TYPE_FENCE_CREATE_INFO};
    rc = vkCreateFence(dev, &fi, NULL, &fence);
    CHECK("vk.create_fence", rc == VK_SUCCESS);
    if (rc)
        goto done;
    VkSubmitInfo si = {
        .sType = VK_STRUCTURE_TYPE_SUBMIT_INFO, .commandBufferCount = 1, .pCommandBuffers = &cb};
    rc = vkQueueSubmit(queue, 1, &si, fence);
    CHECK("vk.submit", rc == VK_SUCCESS);
    if (rc)
        goto done;
    rc = vkWaitForFences(dev, 1, &fence, VK_TRUE, 2000000000ULL);
    CHECK("vk.wait_fence_2s", rc == VK_SUCCESS);
    if (rc)
        goto done;
    uint32_t *ptr = NULL;
    rc = vkMapMemory(dev, mem, 0, 4096, 0, (void **)&ptr);
    CHECK("vk.map_memory", rc == VK_SUCCESS);
    if (rc == VK_SUCCESS) {
        int valid = 1;
        for (unsigned i = 0; i < 1024; i++)
            if (ptr[i] != 0xa5c35a7e)
                valid = 0;
        CHECK("vk.fill_barrier_readback", valid);
        vkUnmapMemory(dev, mem);
    }
done:
    vkDeviceWaitIdle(dev);
    if (fence)
        vkDestroyFence(dev, fence, NULL);
    if (pool)
        vkDestroyCommandPool(dev, pool, NULL);
    if (buf)
        vkDestroyBuffer(dev, buf, NULL);
    if (mem)
        vkFreeMemory(dev, mem, NULL);
    vkDestroyDevice(dev, NULL);
    vkDestroyInstance(instance, NULL);
}
static int run(FILE *f) {
    out = f;
    passes = failures = 0;
    kgsl();
    gles(2);
    gles(3);
    vulkan();
    fprintf(out, "SUMMARY\tpass=%u fail=%u\n", passes, failures);
    fflush(out);
    return failures ? 1 : 0;
}
#ifdef APP_PROBE
JNIEXPORT jint JNICALL Java_org_pocof3_gpuaudit_MainActivity_runWindow(JNIEnv *e, jobject self,
                                                                       jobject surface,
                                                                       jstring path) {
    (void)self;
    const char *p = (*e)->GetStringUTFChars(e, path, NULL);
    out = fopen(p, "a");
    (*e)->ReleaseStringUTFChars(e, path, p);
    if (!out)
        return -1;
    passes = failures = 0;
    ANativeWindow *window = ANativeWindow_fromSurface(e, surface);
    EGLDisplay d = eglGetDisplay(EGL_DEFAULT_DISPLAY);
    EGLSurface surf = EGL_NO_SURFACE;
    EGLContext ctx = EGL_NO_CONTEXT;
    EGLint major, minor, n;
    EGLConfig cfg;
    int ok = window && eglInitialize(d, &major, &minor);
    CHECK("window.egl_initialize", ok);
    if (!ok)
        goto cleanup;
    EGLint attr[] = {EGL_SURFACE_TYPE,
                     EGL_WINDOW_BIT,
                     EGL_RENDERABLE_TYPE,
                     EGL_OPENGL_ES3_BIT_KHR,
                     EGL_RED_SIZE,
                     8,
                     EGL_GREEN_SIZE,
                     8,
                     EGL_BLUE_SIZE,
                     8,
                     EGL_NONE};
    ok = eglChooseConfig(d, attr, &cfg, 1, &n) && n;
    CHECK("window.egl_config", ok);
    if (!ok)
        goto cleanup;
    EGLint ca[] = {EGL_CONTEXT_CLIENT_VERSION, 3, EGL_NONE};
    ctx = eglCreateContext(d, cfg, EGL_NO_CONTEXT, ca);
    surf = eglCreateWindowSurface(d, cfg, window, NULL);
    ok = ctx != EGL_NO_CONTEXT && surf != EGL_NO_SURFACE && eglMakeCurrent(d, surf, surf, ctx);
    CHECK("window.surface_context_current", ok);
    if (!ok)
        goto cleanup;
    EGLint w = 0, h = 0;
    eglQuerySurface(d, surf, EGL_WIDTH, &w);
    eglQuerySurface(d, surf, EGL_HEIGHT, &h);
    CHECK("window.valid_dimensions", w > 0 && h > 0);
    CHECK("window.swap_interval_1", eglSwapInterval(d, 1));
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    glViewport(0, 0, w, h);
    ok = 1;
    for (int i = 0; i < 60; i++) {
        glDisable(GL_SCISSOR_TEST);
        glClearColor(.03f, .04f, .05f, 1);
        glClear(GL_COLOR_BUFFER_BIT);
        glEnable(GL_SCISSOR_TEST);
        glScissor((w - 80) * i / 60, h / 2, 80, 80);
        glClearColor(.1f, .4f, .4f, 1);
        glClear(GL_COLOR_BUFFER_BIT);
        if (!eglSwapBuffers(d, surf) || glGetError() != GL_NO_ERROR) {
            ok = 0;
            break;
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    CHECK("window.60_swaps_without_error", ok);
    INFO("window width=%d height=%d 60-swap-wall-ms=%.3f (not a display FPS measurement)", w, h,
         (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0);
cleanup:
    eglMakeCurrent(d, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT);
    if (ctx != EGL_NO_CONTEXT)
        eglDestroyContext(d, ctx);
    if (surf != EGL_NO_SURFACE)
        eglDestroySurface(d, surf);
    if (d != EGL_NO_DISPLAY)
        eglTerminate(d);
    eglReleaseThread();
    if (window)
        ANativeWindow_release(window);
    fprintf(out, "SUMMARY_WINDOW\tpass=%u fail=%u\n", passes, failures);
    fclose(out);
    return failures ? 1 : 0;
}
JNIEXPORT jint JNICALL Java_org_pocof3_gpuaudit_MainActivity_runNative(JNIEnv *e, jobject self,
                                                                       jstring path) {
    (void)self;
    const char *p = (*e)->GetStringUTFChars(e, path, NULL);
    FILE *f = fopen(p, "w");
    (*e)->ReleaseStringUTFChars(e, path, p);
    if (!f)
        return -1;
    int rc = run(f);
    fclose(f);
    return rc;
}
#else
int main(void) { return run(stdout); }
#endif
