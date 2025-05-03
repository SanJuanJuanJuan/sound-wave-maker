import numpy as np
import sounddevice as sd  # 确保已安装 sounddevice 库
import sys


def generate_stereo_wave(left_freq, right_freq, duration=1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

    # 生成左右声道
    left_channel = 0.3 * np.sin(2 * np.pi * left_freq * t)
    right_channel = 0.3 * np.sin(2 * np.pi * right_freq * t)

    # 合并成立体声 (N x 2 的数组)
    stereo_audio = np.column_stack((left_channel, right_channel))
    return stereo_audio.astype(np.float32)


def play_stereo_audio(left_freq, right_freq):
    try:
        print(f"正在播放：左声道 {left_freq}Hz | 右声道 {right_freq}Hz... (按 Ctrl+C 停止)")
        audio = generate_stereo_wave(left_freq, right_freq)

        with sd.OutputStream(samplerate=44100, channels=2) as stream:
            while True:
                stream.write(audio)

    except KeyboardInterrupt:
        print("\n已停止播放")


if __name__ == "__main__":
    try:
        # 示例输入：440,432 （用逗号分隔）
        input_freq = input("请输入左右声道频率（Hz，用逗号分隔）：")
        left_hz, right_hz = map(float, input_freq.split(','))

        if left_hz <= 0 or right_hz <= 0:
            print("频率必须是正数")
            sys.exit()

        play_stereo_audio(left_hz, right_hz)

    except ValueError:
        print("输入格式错误，请按 左频率,右频率 格式输入（例如：440,432）")