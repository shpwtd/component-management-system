$path = 'templates\index.html'
$content = Get-Content $path -Encoding UTF8 -Raw

$old = '{% set _shelf = (shelves|selectattr("id","equalto",c.shelf_id)|first) if c.shelf_id else None %}<a href="/components/{{ c.id }}/stock/in" style="margin-left:12px;"><strong>{{ c.name }}</strong> ({{ c.quantity }}/{{ c.min_stock }}){% if _shelf %} &middot; {{ _shelf.name }}货架-{{ c.row }}行-{{ c.col }}列{% endif %}</a>'

$new = '<a href="/components/{{ c.id }}/stock/in" style="margin-left:12px;"><strong>{{ c.name }}</strong> ({{ c.quantity }}/{{ c.min_stock }}){% if c._shelf_name %} &middot; {{ c._shelf_name }}货架-{{ c.row }}行-{{ c.col }}列{% endif %}</a>'

if ($content -notlike "*$old*") {
    Write-Host "FAIL: original a-tag not found"
    exit 1
}
$content = $content.Replace($old, $new)

$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($path, $content, $utf8)
Write-Host "OK: template simplified (shelf name now from c._shelf_name)"