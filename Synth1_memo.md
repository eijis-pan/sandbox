## Synth1 macOS 版でセキュリティーのエラーがでた場合

![プラグインが開けないエラー画像](Synth1_images/001_cant_open_clicp.png)
![プラグインが開けないエラー画像2](Synth1_images/007_cant_use_clip.png)

こんなエラーが出た場合の対処方法

---

1. GarageBandのプラグインでSynth1を開く

    ![open_synth1](Synth1_images/000_open_synth1.png)

1. 例のエラーが出ます

    ![cant_open](Synth1_images/001_cant_open.png)

1. システム環境設定を開いて、「セキュリティとプライバシー」を開く

    ![system](Synth1_images/002_system.png)
    ↓
    ![system_security](Synth1_images/003_system_security.png)

1. エラーダイアログの「Finderで表示」ボタンをクリックします。

    ![synth1_blocked](Synth1_images/004_synth1_blocked.png)

    システム環境設定の「ダウンロードしたアプリケーションの実行許可：」の箇所に
    「"Synth1.component"は開発元を確認できないため、使用がブロックされました。」と表示されます。

1. システム環境設定の「このまま許可」ボタンをクリックします。

    ![allow_synth1](Synth1_images/006_allow_synth1.png)

    エラーダイアログは「キャンセル」ボタンを押して、閉じます。

1. GarageBandには「Audio Unitプラグインを使用できません」と表示されます。

    ![cant_use](Synth1_images/007_cant_use.png)

1. もう一度、GarageBandのプラグインでSynth1を開く

    ![re_open_synth1](Synth1_images/008_re_open_synth1.png)

1. エラーダイアログに「開く」ボタンが表示されます。

    ![open_confirm](Synth1_images/009_open_confirm.png)

1. 「開く」ボタンを押すと Synth1 が使用できます。

    ![control_view](Synth1_images/010_control_view.png)

    ※ 表示モードが「Control」になっている場合は「Synth1 Cocoa View」を選択すると変更できます。

    ![can_use_synth1](Synth1_images/011_can_use_synth1.png)

---