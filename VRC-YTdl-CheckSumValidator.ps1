# youtube-dl サイトからチェックサムを取得
#
# 引数1 ParsedJsonOfYoutubeDlReselaseUrl
#   以下のURLレスポンス（Json）を Invoke-RestMethod または ConvertFrom-JSON でParseしたオブジェクト
#   https://api.github.com/repos/ytdl-org/youtube-dl/releases
#
# 引数2 CheckSumAssetName
#   チェックサムの種類を示すキーワード
#   "MD5SUMS" MD5ハッシュ
#   "SHA1SUMS" SHA-1ハッシュ
#
function Get-YTdlRemoteHash{
    param (
        [PSCustomObject]$ParsedJsonOfYoutubeDlReselaseUrl,
        [string]$CheckSumAssetName
    )    

    if(
        ($ParsedJsonOfYoutubeDlReselaseUrl -isnot [array]) -or
        ($ParsedJsonOfYoutubeDlReselaseUrl.Length -lt 1) -or
        ($ParsedJsonOfYoutubeDlReselaseUrl[0].assets -isnot [array]) -or
        ($ParsedJsonOfYoutubeDlReselaseUrl[0].assets.Length -lt 1)
    ) {
        Write-Output $null
        return
    }

    $hashUrl = $null
    foreach($asset in $ParsedJsonOfYoutubeDlReselaseUrl[0].assets){
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
    # レスポンス内容は以下のような形式のテキストファイル
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
