# youtube-dl �T�C�g����`�F�b�N�T�����擾
#
# ����1 ParsedJsonOfYoutubeDlReselaseUrl
#   �ȉ���URL���X�|���X�iJson�j�� Invoke-RestMethod �܂��� ConvertFrom-JSON ��Parse�����I�u�W�F�N�g
#   https://api.github.com/repos/ytdl-org/youtube-dl/releases
#
# ����2 CheckSumAssetName
#   �`�F�b�N�T���̎�ނ������L�[���[�h
#   "MD5SUMS" MD5�n�b�V��
#   "SHA1SUMS" SHA-1�n�b�V��
#
# ����3 TargetReleaseIndex
#   �ȗ��i�ȗ��� 0�j
#   0 �ōŐV�ł̃����[�X������
#
function Get-YTdlRemoteHash{
    param (
        [PSCustomObject]$ParsedJsonOfYoutubeDlReselaseUrl,
        [string]$CheckSumAssetName,
        [int]$TargetReleaseIndex = 0
    )    

    if(
        ($ParsedJsonOfYoutubeDlReselaseUrl -isnot [array]) -or
        ($ParsedJsonOfYoutubeDlReselaseUrl.Length -le $TargetReleaseIndex) -or
        ($ParsedJsonOfYoutubeDlReselaseUrl[$TargetReleaseIndex].assets -isnot [array]) -or
        ($ParsedJsonOfYoutubeDlReselaseUrl[$TargetReleaseIndex].assets.Length -lt 1)
    ) {
        Write-Output $null
        return
    }

    $hashUrl = $null
    foreach($asset in $ParsedJsonOfYoutubeDlReselaseUrl[$TargetReleaseIndex].assets){
        if($asset.name -eq $CheckSumAssetName){
            $hashUrl = $asset.browser_download_url
            break
        }
    }
    if($null -eq $hashUrl){
        Write-Output $null
        return
    }
    $uri = New-Object Uri($hashUrl)
    $cli = New-Object System.Net.WebClient
    $hashResponse = $cli.DownloadString($uri)
    #
    # ���X�|���X���e�͈ȉ��̂悤�Ȍ`���̃e�L�X�g�t�@�C��
    #
    # 9b4ae1f31dee6f6b1d9eaad510ba2698  youtube-dl
    # 35670b38e52443d1d0d6dfbdff574c5e  youtube-dl.exe
    # 86186d02dc16dd4e249bc83eecef4a86  youtube-dl-2020.01.24.tar.gz
    #
    $hashFromWeb = $null
    $hashList = $hashResponse -split("\n")
    foreach($hashLine in $hashList){
        if([string]::IsNullOrEmpty($hashLine)){
            continue
        }
        $hashAndNamePair = $hashLine.Trim() -split("\s+")
        if(
            ($null -eq $hashAndNamePair) -or 
            ($hashAndNamePair.Length -lt 2)     # < 2
            ){
            continue
        }
        $hashValue = $hashAndNamePair[0]
        $hashFileName = $hashAndNamePair[1]
        if(
            [string]::IsNullOrEmpty($hashValue) -or
            [string]::IsNullOrEmpty($hashFileName)
            ){
            continue
        }
        if($hashFileName -eq $exeName) {
            $hashFromWeb = $hashValue
            break
        }
    }

    Write-Output $hashFromWeb
}
